from django import forms

from django.core.validators import MinValueValidator


class DonationForm(forms.Form):
    donation = forms.DecimalField(label="donation amount of money",
                                  required=True,
                                  min_value=.2,
                                  validators=[MinValueValidator(0.2)],
                                  error_messages={'required': "you can't sumbit an empty donation",
                                                  'min_value': "doesn't exceen min donation value"
                                                  })
