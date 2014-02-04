from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User

def get_upload_file_name(instance, filename):
    return "static/img/product_photos/%s" % filename

class Product(models.Model):
    CATEGORIES = (
        ('New', 'NEW'),
        ('Used', 'USED'),
    )
    LANGUAGES = (
        ('Bangla', 'BN'),
        ('English', 'EN'),
        ('Arabia', 'AR'),
    )

    MONEY_CHOICES = (
        ('$', 'USD' ),
        ('BDT', 'BDT'),
    )

    user = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=10, choices=CATEGORIES)
    language = models.CharField(max_length=10, choices=LANGUAGES)
    money_type = models.CharField(max_length=10, choices=MONEY_CHOICES)
    price = models.IntegerField(max_length=10)
    thumbnail = models.FileField(upload_to=get_upload_file_name)
    created_at = models.DateTimeField(default=datetime.datetime.now())

    def __unicode__(self):
        return self.title





#User.profile = property(lambda u: Product.objects.get_or_create(user=u)[0])
