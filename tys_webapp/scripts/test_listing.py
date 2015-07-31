from tys_webapp import services
from tys_webapp.models import EtsyUser

print('Running a test on the listing generator.')
test_user = EtsyUser.objects.get(user__username='anneal')
test_listing = services.SuggestedListing(test_user)
test_listing.generate()
print(test_listing.getListingInfo('listing_id', 'title', 'price', 'who_made',
                                  'is_supply', 'is_digital'))

test_listing.saveToUser()
