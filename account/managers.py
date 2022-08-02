from django.contrib.auth.base_user import BaseUserManager


class MyAccountManager(BaseUserManager):
    """
       Custom user model manager where email is the unique identifiers
       for authentication instead of usernames.
    """
    def create_user(self, fullname, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        if not fullname:
            raise ValueError('Users must have a fullname')

        user = self.model(
            fullname=fullname,
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, fullname, username, email, password=None):
        user = self.create_user(
            fullname=fullname,
            username=username,
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


def get_profile_image_filepath(self, filename):
    return 'profile_images/' + str(self.pk) + '/profile_image.png'


def get_default_profile_image():
    return "beauty_media/default_profile_image.png"


def get_post_filepath(self, filename):
    return 'p/' + str(self.pk) + '.png'
