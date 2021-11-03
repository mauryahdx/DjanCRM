from django.db import models
from django.db.models.signals import post_save, pre_save 
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_organiser = models.BooleanField(default= True)
    is_agent = models.BooleanField(default=False)
    pass 


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.user.username

class Lead(models.Model):

#    SOURCE_CHOICES = (
#        ('YouTube', 'YouTube'),
#        ('Google', 'Google'),
#        ('Newsletter', 'Newsletter'),
#    )

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    agent = models.ForeignKey("Agent", null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey("Category", related_name="leads", null=True, blank=True, on_delete = models.SET_NULL)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

#    phoned = models.BooleanField(default=false)
#    source = models.CharField(choices=SOURCE_CHOICES, max_length=100)
#
#    profile_picture = models.ImageField(blank=True, null=True)
#    special_files = models.FileField(blank=True, null=True)
# Create your models here.

class Agent(models.Model):
    user = models.OneToOneField(User, related_name='user_agent_set',on_delete = models.CASCADE)
    organisation = models.ForeignKey(UserProfile, on_delete =models.CASCADE)
    def __str__(self):
        return self.user.email

class Category(models.Model):
    name = models.CharField(max_length = 30)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(post_user_created_signal, sender=User) 