from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="category",default='no image')

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category ,related_name="Post",on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to="thumb")
    yt_link = models.CharField(max_length=500,blank=True,null=True)
    video = models.FileField(upload_to="videos",blank=True,null=True)
    date = models.DateTimeField(auto_now_add=True)

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None,created=False,**kwargs):
    if created:
        Token.objects.create(user=instance)


