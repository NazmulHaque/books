from django.db import models
from django.contrib.auth.models import User
#from django.db.models.signals import post_save
#from django.dispatch import receiver

from books import settings
# Create your models here.

#import logging
#logr = logging.getLogger(__name__)

def get_upload_file_name(instance, filename):
    return "/static/img/profile-photos/%s" % filename

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    fullname = models.CharField(max_length=200)
    address = models.TextField()
    upozila = models.CharField(max_length=200)
    district = models.CharField(max_length=200, choices=settings.DISTRICT_CHOICES)
    contact_number = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10)
    birthday = models.DateField(null=True, blank=True)
    photo = models.FileField(upload_to=get_upload_file_name, default=settings.DEFAULT_PROFILE_PHOTO)

    def __unicode__(self):
        return self.fullname

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


#@receiver(post_save, sender=User)
#def make_sure_user_profile_is_added_on_user_created(sender, **kwargs):
#    if kwargs.get('created', False):
#        up = UserProfile.objects.create(user=kwargs.get('instance'))
#        logr.debug("UserProfile created: %s" % up)