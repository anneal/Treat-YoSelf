import requests
from requests_oauthlib import OAuth1
from urllib.parse import parse_qs
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseRedirect
from .forms import PreferenceForm, InclusiveKeywordSet, ExclusiveKeywordSet
from .services import *
from .settings import CONSUMER_KEY, CONSUMER_SECRET, \
                      OAUTH_SCOPE, SCOPE_URL_EXT


saved_secret = ''


def index(request):
    if authenticateUserAndLogin(request, request.user) and validOauth(request):
        updateUser(request.user)
        return redirect('/welcome/')
    else:
        if request.method == 'POST':
            return redirect('/oauthlogin/')
        else:
            return render(request,
                          'tys_webapp/index.html')


def welcomePage(request):
    if not validOauth(request) and not request.user.is_authenticated():
        return redirect('/')

    current_user = EtsyUser.objects.get(user=request.user)
    current_pref = getEtsyUserPreferences(current_user)

    if request.method == 'POST':
        form = PreferenceForm(request.POST, instance=current_pref)
        if form.is_valid():
            updated_pref = form.save(commit=False)
            inclusive_key_set = InclusiveKeywordSet(request.POST,
                                                    instance=current_user)
            exclusive_key_set = ExclusiveKeywordSet(request.POST,
                                                    instance=current_user)
            if inclusive_key_set.is_valid() and exclusive_key_set.is_valid():
                updated_pref.save()
                inclusive_key_set.save()
                exclusive_key_set.save()
                return render(request,
                              'tys_webapp/welcome.html',
                              {'form': form,
                               'inclusive_key_set': inclusive_key_set,
                               'exclusive_key_set': exclusive_key_set,
                               'username': request.user.username,
                               'message': 'Preference updates saved.'})
    else:
        form = PreferenceForm(instance=current_pref)
        inclusive_key_set = InclusiveKeywordSet(instance=current_user)
        exclusive_key_set = ExclusiveKeywordSet(instance=current_user)

    return render(request,
                  'tys_webapp/welcome.html',
                  {'form': form,
                   'inclusive_key_set': inclusive_key_set,
                   'exclusive_key_set': exclusive_key_set,
                   'username': request.user.username})


def oauthLogin(request):
    global saved_secret

    try:
        if 'oauth_verifier' in request.GET:
            headeroauth = OAuth1(CONSUMER_KEY,
                                 client_secret=CONSUMER_SECRET,
                                 resource_owner_key=request.GET['oauth_token'],
                                 resource_owner_secret=saved_secret,
                                 verifier=request.GET['oauth_verifier'],
                                 signature_type='auth_header')
            access_url = etsyAPI_URL + '/oauth/access_token'
            response = requests.post(url=access_url, auth=headeroauth)
            credentials = parse_qs(response.text)
            headeroauth = OAuth1(CONSUMER_KEY,
                                 client_secret=CONSUMER_SECRET,
                                 resource_owner_key=credentials['oauth_token'][0],
                                 resource_owner_secret=credentials['oauth_token_secret'][0],
                                 signature_type='auth_header')
            user_url = etsyAPI_URL + '/users/__SELF__'
            response = requests.get(url=user_url, auth=headeroauth)
            user_data = response.json()['results'][0]
            current_user = createUser(user_data['login_name'])
            etsyUser = getEtsyUser(current_user)
            etsyUser.access_token = credentials['oauth_token'][0]
            etsyUser.access_token_secret = credentials['oauth_token_secret'][0]
            etsyUser.save()
            authenticateUserAndLogin(request, current_user)
            return redirect('/')
        else:
            request_url = etsyAPI_URL + '/oauth/request_token' + SCOPE_URL_EXT
            headeroauth = OAuth1(CONSUMER_KEY,
                                 CONSUMER_SECRET,
                                 signature_type='auth_header',
                                 callback_uri='http://127.0.0.1:8000/oauthlogin/')
            response = requests.post(request_url, auth=headeroauth)
            parsed_response = parse_qs(response.text)
            saved_secret = parsed_response['oauth_token_secret'][0]
            return HttpResponseRedirect(parsed_response['login_url'][0])
    except Exception as E:
        print(E)
        return redirect('/')


def logout_view(request):
    if not request.user.is_authenticated():
        return redirect('/')
    else:
        logout(request)
        return redirect('/')
