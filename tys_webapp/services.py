import requests
from requests_oauthlib import OAuth1
from django.contrib.auth import authenticate, login
from .models import User, EtsyUser, Keyword, \
                    UserPreference, UserExcludedKeyword, Listing
from .settings import CONSUMER_KEY, CONSUMER_SECRET


etsyAPI_URL = 'https://openapi.etsy.com/v2'


def validOauth(a_user):
    current_user = EtsyUser.objects.get(user=a_user)
    headeroauth = OAuth1(CONSUMER_KEY,
                         client_secret=CONSUMER_SECRET,
                         resource_owner_key=current_user.access_token,
                         resource_owner_secret=current_user.access_token_secret,
                         signature_type='auth_header')
    user_url = etsyAPI_URL + '/users/__SELF__'
    response = requests.get(url=user_url, auth=headeroauth)
    if response.status_code == 200:
        return True
    else:
        return False


def createUser(validUsername):
    try:
        currentUser = User.objects.get(username=validUsername)
    except User.DoesNotExist:
        currentUser = User.objects.create_user(validUsername,
                                               'abc@gmail.com',
                                               '123')
    currentUser.save()
    return currentUser


def getEtsyUser(a_user):
    try:
        currentUser = EtsyUser.objects.get(user=a_user)
    except EtsyUser.DoesNotExist:
        currentUser = EtsyUser.objects.create(user=a_user)
    currentUser.save()
    return currentUser


def validEtsyUsername(user_input):
    URL_ext = '/users/%s' % user_input
    try:
        getRequestFromEtsy(URL_ext)['results'][0]['user_id']
    except:
        return False
    return True


def authenticateUserAndLogin(request, a_user):
    user = authenticate(username=a_user.username, password='123')
    if user is not None and user.is_active:
        login(request, user)
        return True
    return False


def updateUser(currentUser):
    #TODO add email address
    updateEtsyProfile(currentUser)


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


def getRequestFromEtsy(URL_ext, params=[]):
    return requests.get(generateRequestURL(URL_ext, params)).json()


def oauthRequestToEtsy(URL_ext, current_user, params=[]):
    headeroauth = OAuth1(CONSUMER_KEY,
                         client_secret=CONSUMER_SECRET,
                         resource_owner_key=current_user.access_token,
                         resource_owner_secret=current_user.access_token_secret,
                         signature_type='auth_header')
    response = requests.post(url=generateOauthRequestURL(URL_ext, params),
                            auth=headeroauth)
    if response.status_code == 200:
        return True
    else:
        return False


def generateRequestURL(URL_ext, params=[]):
    paramList = {'api_key': CONSUMER_KEY}
    if params:
        paramList.update(params)
    paramString = ''.join(['&' + key + '=' + paramList[key]
                           for key in paramList])[1:]
    return etsyAPI_URL + URL_ext + '?' + paramString


def generateOauthRequestURL(URL_ext, params=[]):
    paramList = {}
    if params:
        paramList.update(params)
        paramString = ''.join(['&' + key + '=' + paramList[key]
                               for key in paramList])[1:]
        return etsyAPI_URL + URL_ext + '?' + paramString
    else:
        return etsyAPI_URL + URL_ext


def createListing(a_listing_id):
    try:
        currentListing = Listing.objects.get(listing_id=a_listing_id)
    except Listing.DoesNotExist:
        currentListing = Listing(listing_id=a_listing_id)
        currentListing.save()
    return currentListing


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


def resetOrderDate(a_user):
    current_pref = UserPreference.objects.get(user=a_user)
    current_pref.order_date = current_pref.next_order_date
    current_pref.next_order_date
    current_pref.save()


class SuggestedListing():

    MIN_NUM_LISTINGS = 1

    def __init__(self, a_user):
        self.my_etsy_user = a_user
        self.listings = []

    def generate(self):
        self.listings = []
        page = 0
        while len(self.listings) < self.MIN_NUM_LISTINGS:
            page += 1
            response = self.getListingsFromEtsy(page)
            self.listings.extend(self.cleanupListingResults(response))

    def saveToUser(self):
        first_listing = self.listings[0]
        self.my_etsy_user.listing = createListing(first_listing['listing_id'])
        self.my_etsy_user.save()

    def putInCart(self):
        URL_ext = '/users/' + str(self.my_etsy_user.etsy_user_id) + '/carts'
        first_listing = self.listings[0]
        params = {'user_id': str(self.my_etsy_user.etsy_user_id),
                  'listing_id': str(first_listing['listing_id']),
                  'quantity': str(1)}
        if oauthRequestToEtsy(URL_ext, self.my_etsy_user, params):
            self.saveToUser()

    def getListingsFromEtsy(self, page=1):
        URL_ext = '/listings/active'
        self.my_pref = UserPreference.objects.get(user=self.my_etsy_user)
        params = {'limit': str(self.MIN_NUM_LISTINGS + 10),
                  'page': str(page),
                  'max_price': str(self.my_pref.price_max),
                  'min_price': str(self.my_pref.price_min)}
        return getRequestFromEtsy(URL_ext, params)['results']

    def cleanupListingResults(self, rawListings):
        return self.removeHighShippingCost(
                    self.removeNonKeywordListings(
                        self.removeNonHandmadeListings(rawListings)))

    def removeNonHandmadeListings(self, rawListings):
        return [eachListing for eachListing in rawListings
                if eachListing['who_made'] == 'i_did' and
                   eachListing['is_supply'] == 'false' and
                   eachListing['is_digital'] is not True]

    def removeNonKeywordListings(self, rawListings):
        try:
            nonPrefs = UserExcludedKeyword.objects.get(user=self.my_etsy_user)
            nonKeywords = [each.keyword
                           for each in nonPrefs.excluded_keywords.all()]
        except Exception:
            nonKeywords = []

        nonKeywords.append('ADD-ON')

        validListings = []
        for eachListing in rawListings:
            acceptableListing = True
            for keyword in nonKeywords:
                if (keyword in eachListing['category_path'] or
                    keyword in eachListing['title'] or
                    keyword in eachListing['tags']):
                        acceptableListing = False
            if acceptableListing:
                validListings.append(eachListing)
        return validListings

    def removeHighShippingCost(self, rawListings):
        validListings = []
        for eachListing in rawListings:
            listingShippingCost = self.getShippingCost(eachListing)
            totalCost = float(eachListing['price']) + float(listingShippingCost)
            if totalCost <= float(self.my_pref.price_max):
                validListings.append(eachListing)
        return validListings

    def getShippingCost(self, listing):
        country = self.my_etsy_user.etsy_country_id
        listing_id = listing['listing_id']
        URL_ext = '/listings/' + str(listing_id) + '/shipping/info'
        shippingInfo = getRequestFromEtsy(URL_ext)['results']
        shippingCost = [shipProtocol['primary_cost']
                        for shipProtocol in shippingInfo
                        if shipProtocol['destination_country_id'] == country]
        if len(shippingCost) == 0:
            shippingCost = [shipProtocol['primary_cost']
                            for shipProtocol in shippingInfo
                            if shipProtocol['destination_country_name']
                            == 'Everywhere Else']
        if len(shippingCost) == 0:
            shippingCost = [100000]
        return shippingCost[0]

    def getListingInfo(self, *fields):
        results = []
        for listing in self.listings:
            listingInfo = {}
            for key in listing:
                if key in fields:
                    listingInfo[key] = listing[key]
            results.append(listingInfo)
        return results
