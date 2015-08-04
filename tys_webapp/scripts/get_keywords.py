'''
This script can be run occasionaly to update the Etsy keywords.
'''


from tys_webapp import services

print('Running the keyword update file.......')
services.getKeywords()
