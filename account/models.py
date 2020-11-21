from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime


class Client(models.Model):
    client_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.PROTECT)
  
 
    
    def __str__(self):
        return self.user.first_name + " " + \
                          self.user.last_name 
 

    def create_client_profile(sender, **kwargs):
        if kwargs['created']:
            client = Client.objects.create(user=kwargs['instance'])

    post_save.connect(create_client_profile, sender=User)
    








