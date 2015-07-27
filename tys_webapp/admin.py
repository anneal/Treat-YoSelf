from django.contrib import admin
from .models import *


admin.site.register(EtsyUser)
admin.site.register(Keyword)
admin.site.register(UserPreference)
admin.site.register(UserExcludedKeyword)
admin.site.register(UserIncludedKeyword)
admin.site.register(Listing)
