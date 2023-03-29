from django import forms
from user.models import User
from django.contrib.auth import authenticate




class RegistraionForm():
    class Meta:
        model = User
        fields = ('email','username','first_name','last_name','phone','photo','password1','password2')
        
        
        
#==============================================================================================================

#===================================================================================================



class UpdaeData(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','first_name','last_name','phone','photo']
        
        
class OptionalData(forms.ModelForm):
    class Meta:
        model=User
        fields=['country','facebook_link','date_birth']

# class UpdateUserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('first_name','last_name','phone','photo')
    
#     def clean_country(self):
#         if self.is_valid():
#             country = self.cleaned_data['country']
#             if country:
#                 return country
#             else :
#                 return None


    # def clean_facebook_link(self):
    #     if self.is_valid():
    #         facebook_link = self.cleaned_data['facebook_link']
    #         if facebook_link:
    #             return facebook_link
    #         else :
    #             return None


    # def clean_date_birth(self):
    #     if self.is_valid():
    #         date_birth = self.cleaned_data['date_birth']
    #         if date_birth:
    #             return date_birth
    #         else :
    #             return None
    
