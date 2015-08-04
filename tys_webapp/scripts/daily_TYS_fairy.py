'''
This script runs daily to check all user accounts for needed orders.
'''


from datetime import date
from tys_webapp import services
from tys_webapp.models import UserPreference


all_user_prefs = UserPreference.objects.all()

users_needing_listings = [pref.user for pref in all_user_prefs]
                          if date.today() >= pref.order_date]

count = 0
for each in users_needing_listings:
    if services.validOauth(each.user):
        new_listing = services.SuggestedListing(each)
        new_listing.generate()
        new_listing.putInCart()
        services.resetOrderDate(each)
        count += 1

print('TYS listings were placed for %s users.' % count)
