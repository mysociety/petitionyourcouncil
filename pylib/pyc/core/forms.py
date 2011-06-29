import re
from django import forms

from core.models import Council


class CouncilPetitonInfoForm(forms.ModelForm):

    # def clean(self):
    #     cleaned_data = self.cleaned_data
    #     url   = cleaned_data.get("petition_url")
    #     email = cleaned_data.get("contact_email")
    #     
    #     if not( url or email ):
    #         raise forms.ValidationError("Please find a contact email if the petition_url is missing.")
    #     
    #     return cleaned_data
    
    class Meta:
        model = Council
        fields = (
            'petition_url', 'petition_rss',
             # 'contact_email'
        )