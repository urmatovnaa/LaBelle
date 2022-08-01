from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.models import AbstractUser

from account.managers import MyAccountManager, get_profile_image_filepath, get_default_profile_image


class Profession(models.Model):
    name = models.CharField(max_length=60, unique=True)

    def clean(self):
        self.name = self.name.capitalize()
        return self.name

    def __str__(self):
        return f'{self.name}'


class Account(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    first_name = None
    last_name = None

    fullname = models.CharField(max_length=60)
    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[username_validator],
        error_messages={
            "unique": "A user with that username already exists.",
        }, )
    email = models.EmailField(unique=True)
    profile_image = models.ImageField(upload_to=get_profile_image_filepath,
                                      null=True, blank=True,
                                      default=get_default_profile_image)
    info = models.CharField(max_length=255, help_text='timetable, phone_number, location', blank=True, null=True)
    profession = models.ForeignKey(Profession, models.CASCADE, blank=True, null=True)
    web_site = models.URLField(blank=True, null=True)

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname', 'username']

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index('profile_images/' + str(self.pk) + "/"):]

    def __str__(self):
        return f'{self.username}'

