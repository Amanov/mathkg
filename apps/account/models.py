from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User

#creating custom users
class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")
        
        user =self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    #creating superuser/admin
    def create_superuser(self, email, username, password):
        user =self.create_user(
            email=self.normalize_email(email),
            password =password,
            username=username,
        )
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user
        


class Account(AbstractBaseUser):
    email                   = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username                = models.CharField(max_length=30, unique=True)  
    date_joined             = models.DateTimeField(verbose_name='date joined', auto_now_add=True) #date joined
    last_login              = models.DateTimeField(verbose_name='last_login', auto_now=True)
    is_admin                = models.BooleanField(default=False)
    is_active               = models.BooleanField(default=False) #activation of user
    is_staff                = models.BooleanField(default=False)
    is_superuser            = models.BooleanField(default=False)     
    # first_name              =models.CharField(max_length=30) 
    # 
    # ✅ Subscription end date field
    subscription_end = models.DateField(null=True, blank=True)           

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]  #'first_name' we can add a list

    objects = MyAccountManager()


    def __str__(self):
        return self.email  
    
    def has_perm(self, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    

@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False,**kwargs):
    if created:
        Token.objects.create(user=instance)
    else:
        pass

## I want to count how many times file is downloaded
# yourapp/models.py

from django.db import models
from django.utils import timezone

class DownloadFile(models.Model):
    name            = models.CharField(max_length=255)
    file            = models.FileField(upload_to='downloads/')
    slug            = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    
    # ─── add / keep these ───
    download_count  = models.PositiveIntegerField(default=0, editable=False)
    last_downloaded = models.DateTimeField(null=True, blank=True, editable=False)

    def increment_download(self):
        self.download_count += 1
        self.last_downloaded = timezone.now()
        self.save(update_fields=['download_count', 'last_downloaded'])

    def __str__(self):
        return f"{self.name} ({self.download_count})"



