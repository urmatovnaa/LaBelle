from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from account.managers import get_post_filepath
from main_project.settings import AUTH_USER_MODEL


class Post(models.Model):
    """ Model of post """
    post = models.FileField(upload_to=get_post_filepath)
    data_creating = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    likes = GenericRelation('wall_app.Like')

    @property
    def total_likes(self):
        return self.likes.count()

    def get_post_filename(self):
        return str(self.post)[str(self.post).index('post/' + str(self.pk) + "/"):]

    def __str__(self):
        return f'posted by  {self.owner}'


class Like(models.Model):
    """ Post like model """
    user = models.ForeignKey(AUTH_USER_MODEL,
                             related_name='likes',
                             on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Comment(models.Model):
    """ Post comment model """
    user = models.ForeignKey(AUTH_USER_MODEL,
                             related_name='comments',
                             on_delete=models.SET_NULL)
    text = models.CharField(max_length=255)
    data_creating = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL, blank=True, null=True, related_name="children"
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.text} - {self.user}"


class PriceList(models.Model):
    """ Specialist services price list """
    service_name = models.CharField(max_length=255)
    price = models.IntegerField()
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.service_name} - {self.price} '


class Review(models.Model):
    """ Specialist review """
    specialist = models.ForeignKey(AUTH_USER_MODEL,
                                   related_name='reviews',
                                   on_delete=models.SET_NULL,
                                   null=True)
    text = models.CharField(max_length=500)
    data_creating = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL, blank=True, null=True, related_name="children"
    )
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")

    def __str__(self):
        return f"{self.specialist} - {self.text} - {self.owner}"
