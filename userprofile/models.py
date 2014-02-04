from django.db import models
from django.contrib.auth.models import User
#from django.db.models.signals import post_save
#from django.dispatch import receiver

# Create your models here.

#import logging
#logr = logging.getLogger(__name__)

def get_upload_file_name(instance, filename):
    return "static/img/profile_photos/%s" % filename


class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('MALE', 'Male',),
        ('FEMALE', 'Female',),
    )
    user = models.OneToOneField(User)
    fullname = models.CharField(max_length=200, null=True)
    contact_address = models.TextField(null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True)
    date_of_birth = models.DateField(null=True)
    contact_number = models.IntegerField(null=True)
    profile_photo = models.FileField(upload_to=get_upload_file_name)

    def __unicode__(self):
        return self.fullname


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


#@receiver(post_save, sender=User)
#def make_sure_user_profile_is_added_on_user_created(sender, **kwargs):
#    if kwargs.get('created', False):
#        up = UserProfile.objects.create(user=kwargs.get('instance'))
#        logr.debug("UserProfile created: %s" % up)