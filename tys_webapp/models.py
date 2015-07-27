from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


""" The imported User class includes the following:
        username
        first_name
        last_name
        email
        password
        groups
        user_permissions
        is_staff
        is_active
        is_superuser
        last_login
        date_joined
"""


class Keyword(models.Model):
    keyword = models.CharField(max_length=200, default='')
    keyword_id = models.PositiveIntegerField(primary_key=True)
    keyword_desc = models.CharField(max_length=200)

    def __str__(self):
        return self.keyword_desc


class Listing(models.Model):
    listing_id = models.CharField(max_length=10, default='null')

    def __str__(self):
        return self.listing_id


class EtsyUser(models.Model):
    user = models.OneToOneField(User)
    etsy_user_id = models.PositiveIntegerField(default=0)
    etsy_gender = models.CharField(max_length=100, default='')
    etsy_country_id = models.PositiveIntegerField(default=0, null=True)
    listing = models.ForeignKey(Listing, blank=True, null=True)

    def __str__(self):
        return 'Etsy User ID: %s' % self.etsy_user_id


class UserPreference(models.Model):
    user = models.OneToOneField(EtsyUser)
    ship_frequency = models.PositiveIntegerField(default=14)
    next_ship_date = models.DateField(default=timezone.now)
    price_max = models.DecimalField(max_digits=8,
                                    decimal_places=2,
                                    default=25.00)
    price_min = models.DecimalField(max_digits=8,
                                    decimal_places=2,
                                    default=0.00)

    def __str__(self):
        return str(self.next_ship_date)


class UserExcludedKeyword(models.Model):
    user = models.ForeignKey(EtsyUser)
    excluded_keywords = models.ForeignKey(Keyword, blank=True, null=True)

    def __str__(self):
        return str(self.excluded_keywords)


class UserIncludedKeyword(models.Model):
    user = models.ForeignKey(EtsyUser)
    included_keywords = models.ForeignKey(Keyword, blank=True, null=True)

    def __str__(self):
        return str(self.included_keywords)
