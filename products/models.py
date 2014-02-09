from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User

from books import  settings

def get_upload_file_name(filename):
    return "/static/img/product-photos/%s" % filename

class Products(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=10, choices=settings.PRODUCT_CATEGORY)
    condition = models.CharField(max_length=10, choices=settings.PRODUCT_CONDITION)
    language = models.CharField(max_length=10, choices=settings.PRODUCT_LANGUAGES)
    money_type = models.CharField(max_length=10, default='BDT')
    price = models.IntegerField(max_length=10)
    thumbnail = models.FileField(upload_to=get_upload_file_name, default=settings.DEFAULT_PRODUCT_PHOTO)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(default=datetime.datetime.now())
    status = models.CharField(max_length=10, choices=settings.PRODUCT_STATUS, default='Approval')

    def __unicode__(self):
        return self.title
