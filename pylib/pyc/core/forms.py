import re
from django import forms

from core.models import Council


class CouncilPetitonInfoForm(forms.ModelForm):
    class Meta:
        model = Council
        fields = ( 'petition_url', 'petition_rss' )