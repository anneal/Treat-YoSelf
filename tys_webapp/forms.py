from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from .models import EtsyUser, UserPreference, \
                    UserIncludedKeyword, UserExcludedKeyword


class PreferenceForm(ModelForm):
    class Meta:
        model = UserPreference
        fields = ['ship_frequency',
                  'next_ship_date',
                  'price_min',
                  'price_max']

InclusiveKeywordSet = inlineformset_factory(EtsyUser,
                                            UserIncludedKeyword,
                                            fields=('included_keywords',),
                                            can_delete=False,
                                            max_num=1)

ExclusiveKeywordSet = inlineformset_factory(EtsyUser,
                                            UserExcludedKeyword,
                                            fields=('excluded_keywords',),
                                            can_delete=False,
                                            max_num=1)
