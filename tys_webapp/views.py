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

token_secret = ''

def oauthLogin(request):
    request_url = etsyAPI_URL + '/oauth/request_token' + SCOPE_URL_EXT
    headeroauth = OAuth1(CONSUMER_KEY,
                         CONSUMER_SECRET,
                         signature_type='auth_header',
                         callback_uri='http://127.0.0.1:8000/welcome')
    response = requests.post(request_url, auth=headeroauth)
    parsed_response = parse_qs(response.text)
    token = parsed_response['oauth_token'][0]
    token_secret = parsed_response['oauth_token_secret'][0]
    print('HERE')
    return HttpResponseRedirect(parsed_response['login_url'][0])


def index(request):
    if not request.user.is_authenticated():
        return redirect('/login/')
    else:
        return redirect('/welcome/')


def logout_view(request):
    logout(request)
    return redirect('/')


def loginPage(request):
    if request.method == 'POST':
        input_user_id = request.POST['user_id']
        if (validEtsyUsername(input_user_id) and
             authenticateUserAndLogin(request, updateUser(input_user_id))):
                updateUser(input_user_id)
                return redirect('/oauthlogin/')
        else:
            return render(request,
                          'tys_webapp/login.html',
                          {'message':
                           'Invalid username entered. Try again?'})
    return render(request, 'tys_webapp/login.html')


def welcomePage(request):
    if not request.user.is_authenticated():
        return redirect('/login/')

    print(token_secret)

    headeroauth = OAuth1(CONSUMER_KEY,
                         CONSUMER_SECRET,
                         request.GET['oauth_token'],
                         token_secret,
                         request.GET['oauth_verifier'],
                         signature_type='auth_header')
    response = requests.post(etsyAPI_URL + '/access_token', auth=headeroauth)
    credentials = parse_qs(response.text)
    # TODO save credentials to database

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
                return HttpResponse('Successful update')
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
