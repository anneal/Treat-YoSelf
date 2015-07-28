from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

from .models import User, EtsyUser, Keyword, UserPreference
from .forms import PreferenceForm, InclusiveKeywordSet, ExclusiveKeywordSet

import requests


etsyAPI_URL = 'https://openapi.etsy.com/v2'


########################################################################
###    VIEWS
########################################################################


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'tys_webapp/index.html')
    else:
        return redirect('/welcome/')


def loginPage(request):
    if request.method == 'POST':
        input_user_id = request.POST['user_id']
        if (validEtsyUsername(input_user_id) and
             authenticateUserAndLogin(request, updateUser(input_user_id))):
                updateUser(input_user_id)
                return redirect('/welcome/')
        else:
            return render(request,
                          'tys_webapp/login.html',
                          {'message':
                           'Invalid username/password entered. Try again?'})
    return render(request, 'tys_webapp/login.html')


def welcomePage(request):
    if not request.user.is_authenticated():
        return redirect('/login/')

    current_user = EtsyUser.objects.get(user=request.user)
    current_pref = getEtsyUserPreferences(current_user)

    if request.method == 'POST':
        form = PreferenceForm(request.POST, instance=current_pref)
        if form.is_valid():
            updated_pref = form.save(commit=False)
            print(updated_pref)
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


########################################################################
###    OTHER FUNCTIONS
########################################################################


def authenticateUserAndLogin(request, validUsername):
    user = authenticate(username=validUsername, password='123')
    if user is not None and user.is_active:
        login(request, user)
        return True
    return False


def updateUser(validUsername):
    try:
        currentUser = User.objects.get(username=validUsername)
    except User.DoesNotExist:
        currentUser = User.objects.create_user(validUsername,
                                               'abc@gmail.com',
                                               '123')
        currentUser.save()
    updateEtsyProfile(currentUser)
    return currentUser.username


def updateEtsyProfile(a_user):
    URL_ext = '/users/%s/profile' % a_user.username
    response = getRequestFromEtsy(URL_ext)['results'][0]
    try:
        currentUser = EtsyUser.objects.get(user__username=a_user)
    except EtsyUser.DoesNotExist:
        currentUser = EtsyUser(user=a_user)
    currentUser.etsy_user_id = response['user_id']
    currentUser.etsy_gender = response['gender']
    currentUser.etsy_country_id = response['country_id']
    if response['first_name']:
        currentUser.user.first_name = response['first_name']
    if response['last_name']:
        currentUser.user.last_name = response['last_name']
    currentUser.user.save()
    currentUser.save()


def getEtsyUserPreferences(a_user):
    try:
        currentPref = UserPreference.objects.get(user=a_user)
    except UserPreference.DoesNotExist:
        currentPref = UserPreference(user=a_user)
        currentPref.save()
    return currentPref


def validEtsyUsername(user_input):
    URL_ext = '/users/%s' % user_input
    try:
        getRequestFromEtsy(URL_ext)['results'][0]['user_id']
    except:
        return False
    return True


def getRequestFromEtsy(URL_ext, params=[]):
    return requests.get(generateRequestURL(URL_ext, params)).json()


## TODO from apiSettings import my_etsy_api_key
def generateRequestURL(URL_ext, params=[]):
    paramList = {'api_key': 'yrgd2tnzkt0ig8auwvft75b0'}
    if params:
        paramList.update(params)
    paramString = ''.join(['&' + key + '=' + paramList[key]
                            for key in paramList])[1:]
    return etsyAPI_URL + URL_ext + '?' + paramString


def getKeywords():
    URL_ext = '/taxonomy/categories'
    response = getRequestFromEtsy(URL_ext)['results']
    for category in response:
        addKeyword(category)
        numSubcategories = int(category['num_children'])
        """
        if numSubcategories > 0:
            name = category['name']
            getSubkeywords(URL_ext + '/' + name)
        """

def addKeyword(category):
    ID = category['category_id']
    name = category['name']
    desc = category['long_name']
    try:
        currentKeyword = Keyword.objects.get(keyword_ID=ID)
    except Keyword.DoesNotExist:
        currentKeyword = Keyword(keyword_ID=ID)
    currentKeyword.keyword = name
    currentKeyword.keyword_desc = desc
    currentKeyword.save()


def getSubkeywords(URL_ext):
    response = getRequestFromEtsy(URL_ext)['results']
    for category in response:
        addKeyword(category)
        numSubcategories = int(category['num_children'])
        if numSubcategories > 0:
            name = category['name']
            getSubkeywords(URL_ext + '/' + name)
    return True
