import uuid
import os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings

# Create your models here.


def recipe_image_file_path(instance, filename):

    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('upload/recipe', filename)


class UserManager(BaseUserManager):

    def create_user(self, password=None, **extra_fields):

        user = self.model(**extra_fields)

        user.set_password(password)

        user.save(using=self.db)

        return user

    def create_superuser(self, **extra_fields):

        user = self.create_user(**extra_fields)
        user.is_staff = True
        user.is_superuser = True

        user.save()

        return user


class UserModel(AbstractBaseUser, PermissionsMixin):

    #  "email": "testuser@gmail.com",
    #  "email_verified": "true",
    #  "name" : "Test User",
    #  "picture": "https://lh4.googleusercontent.com/-kYgzyAWpZzJ/ABCDEFGHI/AAAJKLMNOP/tIXL9Ir44LE/s99-c/photo.jpg",
    #  "given_name": "Test",
    #  "family_name": "User",
    #  "locale": "en"

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    picture = models.URLField(default=None, blank=True, null=True)
    given_name = models.CharField(max_length=255)
    family_name = models.CharField(max_length=255, blank=True)
    user_name = models.CharField(
        max_length=255, unique=True, null=False, blank=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'user_name'

    objects = UserManager()


class Trip(models.Model):

    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name='organizer'
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    additional_info = models.TextField(null=True)
    extra_people = models.ManyToManyField('UserModel', related_name='member')
    start_lat = models.DecimalField(max_digits=15, decimal_places=6)
    start_lon = models.DecimalField(max_digits=15, decimal_places=6)
    end_lat = models.DecimalField(max_digits=15, decimal_places=6)
    end_lon = models.DecimalField(max_digits=15, decimal_places=6)
    start_name = models.CharField(max_length=255)
    dest_name = models.CharField(max_length=255)
    voters = models.ManyToManyField('UserModel', related_name='voter')
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)


class TripRequest(models.Model):
    trip = models.ForeignKey('Trip', on_delete=models.CASCADE)
    requesters = models.ManyToManyField('UserModel')
