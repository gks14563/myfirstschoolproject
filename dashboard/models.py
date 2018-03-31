from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils.safestring import mark_safe
from django.db.models.signals import pre_save
from django.db.models import signals
from django.core.mail import send_mail




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return "%s" % self.user
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class KYCdata(models.Model):
    class Meta:
        verbose_name_plural = "KYCdata"
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    aadhaar = models.ImageField(upload_to= 'media/aadhaar/', blank=True)
    PAN = models.ImageField(upload_to='media/pan/', blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_KYCverified = models.BooleanField(default=False)
    key_generated = models.BooleanField(default=False)


    def admin_photo(self):
        # used in the admin site model as a "thumbnail"
        return '<img src="%s" height="150"/>' % self.aadhaar.url
    admin_photo.allow_tags = True

    admin_photo.short_description = 'aadhaar'

    def __str__(self):
        return "%s" % self.user

class keychain(models.Model):
    username = models.CharField(max_length=50)
    network = models.CharField(max_length=50, default = 'not assigned')
    public_key_x = models.CharField(max_length=300, default = 'not assigned')
    public_key_y = models.CharField(max_length=300, default='not assigned')
    private_key = models.CharField(max_length=300, default = 'not assigned')
    sec = models.CharField(max_length=300, default = 'not assigned')
    coinAddress = models.CharField(max_length=300, default = 'not assigned')


@receiver(post_save, sender=User)
def update_KYCdata(sender, instance, created, **kwargs):
    if created:
        KYCdata.objects.create(user=instance)
    instance.kycdata.save()
# @receiver(post_save, sender=User)
# def save_KYCdata(sender, instance, **kwargs):
#
#signal used for is_active=False to is_active=True
