from django.db import models

# Create your models here.

from django.shortcuts import get_object_or_404


class Tags(models.Model):
    caption = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return f"{self.caption} "

    @classmethod
    def get_spesific_tag(cls, caption):
        print("---------", caption)
        return cls.objects.filter(caption=caption)
