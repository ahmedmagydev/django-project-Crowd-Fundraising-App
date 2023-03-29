from django.db.models import Sum
from django_enum import EnumField
from django.db import models
from django.shortcuts import reverse, get_object_or_404
from django.contrib.postgres.fields import ArrayField
from categories.models import Categories
# from comments.models import Comments
from django.db.models import Avg
from djmoney.models.validators import MaxMoneyValidator, MinMoneyValidator

from accounts.models import UserProfile
# Create your models here.
from user.models import User
from djmoney.models.fields import MoneyField
from django.utils.text import slugify
from tags.models import Tags

from django_jsonform.models.fields import ArrayField

# from rate.models import Rating, ReportOption
# Create your models here.
from user.models import User


LABEL_CHOICES = (
    ('streeet', ' From the streets to safety'),
    ('wish', ' I wish to feed the orangutans'),
    ('volunteer', 'Nemo enim ipsam voluptatem quia'),
    ('entity', 'single entity'),
    ('principle', 'Successive principle:'),
    ('order', 'Made to order:')
)


class Project(models.Model):
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="user_project")

    title = models.CharField(max_length=100)
    slug = models.SlugField(default="", null=True, blank=True)
    details = models.TextField(null=True, blank=True)

    is_approved = models.BooleanField(default=False)
    features = ArrayField(
        models.CharField(max_length=100, blank=True),
        default=list,
        blank=True
    )

    target_budget = MoneyField(max_digits=14, decimal_places=2,
                               default_currency='USD', default=0, null=False,
                               validators=[
                                   MinMoneyValidator(10),
                                   MaxMoneyValidator(1500)]
                               )

    # total_donation = MoneyField(max_digits=14, decimal_places=2,
    #                             default_currency='USD', default=0)
    # donation = models.ForeignKey(Do, on_delete=models.CASCADE, null=True,
    #                              related_name='project_category', blank=True)
    # # tags
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    start_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    end_at = models.DateTimeField(null=True)

    category = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True,
                                 related_name='project_category', blank=True)
    # tags
    tags = models.ManyToManyField(
        Tags, blank=True, related_name="project_tags")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    # def get_project_avg_rate(self, id):
    #     rate_lst = Rating.objects.filter(
    #         project=self)

    #     avg = round(rate_lst.aggregate(Avg("rate"))["rate__avg"], 2)
    #     return avg

    # @classmethod
    # def get_project_number_of_reports(self):
    #     return ReportOption.objects.filter(project=self).count()

    @classmethod
    def get_projects(cls):
        return cls.objects.all().order_by("-updated_at")

    @classmethod
    def get_approved_projects(cls):
        return cls.objects.filter(is_approved=True).order_by("-updated_at")

    @classmethod
    def get_one_project(cls, id):
        try:
            return get_object_or_404(cls, pk=id)
        except Exception as e:
            return None

    @classmethod
    def filter_projects_by_title(cls, title):
        try:
            res = cls.objects.filter(title__contains=title)
            return res
        except Exception as e:
            return None

    @classmethod
    def filter_projects_by_category(cls, category):
        return cls.objects.filter(category=category)
        # try:
        #     print("c000000000000t", category)
        #     res = cls.objects.filter(category=category)
        #     print("-----------", res)
        #     return res
        # except Exception as e:
        #     return None

    @classmethod
    def filter_projects_by_tag(cls, tag):

        return cls.objects.filter(tags__caption__in=tag)

    @classmethod
    def filter_projects_by_slug(cls, slug):
        try:
            res = cls.objects.filter(slug__contains=slug)
            return res
        except Exception as e:
            return None

    @classmethod
    def get_top_rated_projects(cls):
        # dsc order
        top_rated = cls.objects.order_by("-rate")
        return top_rated

    @classmethod
    def get_recently_created_projects(cls):
        # dsc order
        res = cls.objects.order_by("-created_at")[:6]
        return res

    def get_spefic_project(self):
        try:
            return reverse('', args={self.id})
        except Exception as e:
            return None

    def get_title(self):
        return self.title

    def get_delete_url(self):
        return reverse('', args={self.id})

    def get_edit_url(self):
        return reverse('', args={self.id})

    def get_image_url(self):
        return f"/media/{self.image}"

    def get_spefic_project_by_slug(self):

        try:
            return reverse('', args={self.slug})
        except Exception as e:
            return None

    def get_image_url(self):
        return f"/media/{self.image}"


class Image(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/images')


class Donate(models.Model):
    # user
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="user_donation")

    project = models.ForeignKey(Project, on_delete=models.CASCADE,
                                related_name='project_Donation')

    amount_of_donation = MoneyField(max_digits=14, decimal_places=2,
                                    default_currency='USD', default=0, null=False,
                                    validators=[
                                        MinMoneyValidator(10),
                                        MaxMoneyValidator(1500)]
                                    )

    @classmethod
    def get_total_donation_for_project(cls, project):
        # City.objects.values('name', 'country__name').annotate(Sum('population'))
        # print("pppppppppppppp", cls.objects.filter(project=project))
        total_donation = cls.objects.filter(project=project).aggregate(
            Sum("amount_of_donation"))['amount_of_donation__sum']

        return total_donation if total_donation else 0

    @classmethod
    def donate_by_20(cls, project):
        pass
