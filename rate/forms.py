from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from .models import Project,Rating
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.validators import MaxValueValidator,MinValueValidator

class RateForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rate']
   
    rate = forms.IntegerField(max_value=5,min_value=1)
   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'rate',
            Submit('submit', 'Submit', css_class='btn-success')
        )
    def clean_rate(self):
        rate = self.cleaned_data['rate']
        if rate < 1 or rate > 5:
            raise ValidationError('Rate must be between 1 and 5.')
        return rate