from .models import User, EtsyUser, Keyword, UserPreference
from django.contrib.auth import authenticate, login

import requests


etsyAPI_URL = 'https://openapi.etsy.com/v2'


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
    print('Heading to Etsy to get the keywords')
    URL_ext = '/taxonomy/categories'
    response = getRequestFromEtsy(URL_ext)['results']
    for category in response:
        addKeyword(category)
        numSubcategories = int(category['num_children'])
        if numSubcategories > 0:
            name = category['name']
            getSubkeywords(URL_ext + '/' + name)
    print('All keywords successfully updated.')


def addKeyword(category):
    ID = category['category_id']
    name = category['name']
    desc = category['long_name']
    try:
        currentKeyword = Keyword.objects.get(keyword_id=ID)
    except Keyword.DoesNotExist:
        currentKeyword = Keyword(keyword_id=ID)
    currentKeyword.keyword = name
    currentKeyword.keyword_desc = desc
    currentKeyword.save()
    print('Keyword confirmed in the database: %s' % desc)


def getSubkeywords(URL_ext):
    response = getRequestFromEtsy(URL_ext)['results']
    for category in response:
        addKeyword(category)
        numSubcategories = int(category['num_children'])
        if numSubcategories > 0:
            name = category['name']
            getSubkeywords(URL_ext + '/' + name)
    return True
