from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.models import AbstractUser

from main_project.settings import AUTH_USER_MODEL
from account.managers import MyAccountManager, get_default_profile_image


class Profession(models.Model):
    """ Model of categories/professions """
    name = models.CharField(max_length=60, unique=True)

    def clean(self):
        self.name = self.name.capitalize()

    def __str__(self):
        return f'{self.name}'


class Account(AbstractUser):
    """ My user model """
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
    profile_image = models.ImageField(upload_to='avatars',
                                      null=True, blank=True,
                                      default=get_default_profile_image)
    info = models.CharField(max_length=255, help_text='timetable, phone_number, location', blank=True, null=True)
    profession = models.ForeignKey(Profession, on_delete=models.CASCADE, blank=True, null=True)
    web_site = models.URLField(blank=True, null=True)
    following = models.ManyToManyField('self',
                                       through='account.Contact',
                                       related_name='followers',
                                       symmetrical=False)

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname', 'username']

    def __str__(self):
        return f'{self.username}'


class Rating(models.Model):
    """ Rating for specialists """
    RATE_CHOICES = (
        (1, '1'), (2, '2'),
        (3, '3'), (4, '4'),
        (5, '5'), (6, '6'),
        (7, '7'), (8, '8'),
        (9, '9'), (10, '10'),
    )
    specialist = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rating')
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.SET_NULL)
    star = models.FloatField('Рейтинг', choices=RATE_CHOICES, null=True)

    def __str__(self):
        return f'{self.star} - {self.specialist.username} by {self.user.username}'

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


class Contact(models.Model):
    user_from = models.ForeignKey(AUTH_USER_MODEL,
                                  related_name='rel_from_set',
                                  on_delete=models.CASCADE)
    user_to = models.ForeignKey(AUTH_USER_MODEL,
                                related_name='rel_to_set',
                                on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'


