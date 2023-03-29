from django import forms
from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django.utils.text import slugify
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from .models import Project, Categories, Tags,Image
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.validators import MaxValueValidator,MinValueValidator

class NewProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'details', 'features', 'target_budget', 'category', 'tags', 'end_at']

    image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        required=False,
    )
    target_budget = forms.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(10),MaxValueValidator(1500)]
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tags.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    end_at = forms.DateField(
        label='End Date',
        widget=forms.DateInput(attrs={
            'type': 'date', 'required': True
        }),
        help_text='Enter the end date for your project.'
    )
    title = forms.CharField(
        label='Project Title',
        max_length=50,
        help_text='Enter your project Title.'
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Project Details',
                'title',
                'details',
                'features',
                'image',
                'target_budget',
                'category',
                'tags',
                'end_at',
            ),
            ButtonHolder(
                Submit('submit', 'Submit Now!')
            )
        )
    def clean_target_budget(self):
        target_budget = self.cleaned_data['target_budget']
        if target_budget > 1500 or target_budget < 10:
            raise forms.ValidationError("The value for target budget must be between $10 & $1500 .")
        return target_budget
    def clean_end_at(self):
        end_at = self.cleaned_data['end_at']
        if end_at < timezone.now().date():
            raise ValidationError("End date must be in the future.")
        return end_at
    # def clean_start_at(self):
    #     start_at = self.cleaned_data['start_at']
    #     if start_at >timezone.now().date():
    #         raise ValidationError("Start date must further than now.")
    #     return start_at

    





class Project_Image_Form(forms.ModelForm):
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Image
        fields = ('images',)
















# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth.models import User
# from django import forms
# from .models import Project
# INPUT_CLASSES = 'text-info'

# from django import forms
# from django.forms import formset_factory
# from django.forms.widgets import ClearableFileInput
# from django.core.exceptions import ValidationError
# from django.utils import timezone


# class NewProjectForm(forms.ModelForm):
#     image = forms.ImageField(widget=ClearableFileInput(attrs={'multiple': True}), required=False)
#     features = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
#     tags = forms.CharField(widget=forms.TextInput(attrs={'multiple': True, 'class': 'form-control'}))

#     class Meta:
#         model = Project
#         fields = ['title', 'slug', 'details', 'image', 'features', 'target_budget', 'total_donation', 'end_at', 'category', 'tags']
#         widgets = {
#             'title': forms.TextInput(attrs={'class': 'form-control'}),
#             'details': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
#             'target_budget': forms.NumberInput(attrs={'class': 'form-control'}),
#             'total_donation': forms.NumberInput(attrs={'class': 'form-control'}),
#             'end_at': forms.DateTimeInput(attrs={ 'type': 'date' ,'class': 'form-control datetimepicker-input', 'data-target': '#datetimepicker1'}),
#             'category': forms.Select(attrs={'class': 'form-control'}),
#                 }
#         labels = {
#             'title':('Title'),
#             'slug':('Slug'),
#             'details':('Details'),
#             'image':('Image'),
#             'features':('Features'),
#             'target_budget':('Target budget'),
#             'total_donation':('Total donation'),
#             'end_at':('End at'),
#             'category':('Category'),
#             'tags':('Tags'),
#         }

#     def clean_end_at(self):
#         end_at = self.cleaned_data.get('end_at')
#         if end_at and end_at < timezone.now():
#             raise ValidationError(('The end date/time cannot be in the past.'))
#         return end_at

# class NewProjectForm(forms.ModelForm):
#     title = forms.CharField(
#         label='Project Title',
#         max_length=100,
#         help_text='Enter the title of your project.'
#     )
#     details = forms.CharField(
#         label='Project Details',
#         widget=forms.Textarea(attrs={'rows': 3}),
#         help_text='Enter details about your project.'
#     )
#     features = forms.CharField(
#         label='Project Features',
#         widget=forms.Textarea(attrs={'rows': 3}),
#         help_text='Enter features of your project.'
#     )
#     image = forms.ImageField(
#         label='Project Image',
#         help_text='Upload an image for your project.'
#     )
#     target_budget = forms.IntegerField(
#         label='Target Budget',
#         help_text='Enter the target budget for your project.'
#     )
#     slug = forms.SlugField(
#         label='Project Slug',
#         help_text='Enter a URL-friendly slug for your project.'
#     )
#     end_at = forms.DateField(
#         label='End Date',
#         widget=forms.DateInput(attrs={
#             'type': 'date', 'required': True
#         }),
#         help_text='Enter the end date for your project.'
#     )

#     class Meta:
#         model = Project
#         fields = ('title', 'details', 'features', 'image',
#                   'end_at', 'target_budget', 'slug',)


# class NewProjectForm(forms.ModelForm):
#     class Meta:
#         model = Project
#         # fields = ('title',)
#         fields = ('title', 'details', 'features', 'image',
#                   'end_at', 'target_budget', 'slug',)

#         title = forms.CharField()
#         target_budget = forms.IntegerField()
#         slug = forms.SlugField()
#         end_at=forms.DateField()
#         widgets = {
#             'end_at': forms.DateField(attrs={
#                 'type': 'date', 'required':True
#             }),
#         }



















        # labels={
        #     'title': ' Project Title',
        # }
        # error_messages={
        #     'title': {
        #     'required': 'Please enter a title for your project.',
        #     'max_length': 'Project title must be less than 50 characters.',
        #     'invalid': 'Project title must be alphanumeric and contain no spaces.',
        #     },

        # }
        # widgets = {
        #     'category': forms.Select(attrs={
        #         'class': INPUT_CLASSES, 'required':True
        #     }),
        #      'title': forms.CharField(attrs={
        #         'class': INPUT_CLASSES, 'required':True
        #     }),
        #     'name': forms.TextInput(attrs={
        #         'class': INPUT_CLASSES
        #     }),
        #     'description': forms.Textarea(attrs={
        #         'class': INPUT_CLASSES
        #     }),
        #     'price': forms.TextInput(attrs={
        #         'class': INPUT_CLASSES
        #     }),
        #     'image': forms.FileInput(attrs={
        #         'class': INPUT_CLASSES
        #     })
        # }

        # widgets = {
        # 'title': forms.CharField(attrs={'placeholder': 'Your Name'}),
        #     'details': forms.Textarea(attrs={'placeholder': 'Your Description', 'class': 'form-control', 'id': 'exampleInputdescription'}),
        #     'features': forms.Textarea(attrs={'placeholder': 'Your Description', 'class': 'form-control', 'id': 'exampleInputdescription'}),
        #     'image': forms.ImageField(attrs={'class': 'form-control', 'id': 'exampleInputimage'}),
        #     'end_at':forms.DateTimeField(attrs={'class': 'form-control'}),
        #     'start_at':forms.DateTimeField(attrs={'class': 'form-control'}),
        #     'category': forms.Select(attrs={'class': 'form-control', 'id': 'exampleFormControlSelect1'}),
        #     'target_budget':forms.FloatField(attrs={'class': 'form-control'}),
        #     'tags':forms.MultiValueField(attrs={'class': 'form-control'}),
        #     'slug':forms.SlugField(attrs={'class': 'form-control'})
        # }

    #     class ImageForm(forms.Form):
    # image = forms.ImageField(
    #     widget = forms.FileInput(
    #         attrs = {"id" : "image_field" , # you can access your image field with this id for css styling .
    #                 , style = "height: 100px ; width : 100px ; " # add style from here .
    #                 }
    #         )
