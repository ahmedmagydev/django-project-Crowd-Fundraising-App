from django.db import models

# Create your models here.

# Create your models here.
from django.core.validators import RegexValidator



class User(models.Model):
    id= models.AutoField(primary_key=True)
    phone_regex = RegexValidator(regex=r'^01[1|0|2|5][0-9]{8}$',message='phone must be an egyptian phone number...')
    username = models.CharField(verbose_name="user_name" ,null=False, max_length=50)
    first_name = models.CharField(verbose_name="first_name" ,null=False, max_length=50)
    last_name = models.CharField(verbose_name= "last_name" ,null=False, max_length=50)
    email = models.EmailField(verbose_name='email', null=False, max_length=150,unique=True)
    phone = models.CharField(verbose_name="phone",null=True,validators=[phone_regex],max_length=14)
    photo = models.ImageField(verbose_name="photo",upload_to='images')
    is_active = models.BooleanField(default=False)
    facebook_link=models.CharField(max_length=100,null=True,blank=True)
    country=models.CharField(max_length=20,null=True,blank=True)
    date_birth=models.CharField(max_length=10,null=True,blank=True)
    
    
    def __int__(self):
        return self.id
    
    