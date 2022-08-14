from django.db import models

from main_project.settings import AUTH_USER_MODEL


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Тег')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Image(models.Model):
    image = models.ImageField(verbose_name='Изображение', upload_to='post')
    post = models.ForeignKey('wall_app.Post', related_name='image', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'

    def __str__(self):
        return self.image


class Post(models.Model):
    """ Model of post """
    data_creating = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name='Теги', blank=True)

    def __str__(self):
        return f'posted by  {self.owner}'

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"


class Like(models.Model):
    """ Post like model """
    user = models.ForeignKey(AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey('wall_app.Post', on_delete=models.CASCADE, related_name='likes')


class Comment(models.Model):
    """ Post comment model """
    user = models.ForeignKey(AUTH_USER_MODEL,
                             related_name='comments',
                             on_delete=models.SET_NULL,
                             null=True)
    text = models.CharField(max_length=255)
    data_creating = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL, blank=True, null=True, related_name="children"
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.user} - {self.post}"

    class Meta:
        verbose_name = "Коммент"
        verbose_name_plural = "Комменты"


class PriceList(models.Model):
    """ Specialist services price list """
    service_name = models.CharField(max_length=255)
    price = models.IntegerField()
    specialist = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pricelist')

    def __str__(self):
        return f'{self.service_name} - {self.price} '

    class Meta:
        verbose_name = "Прайс лист"
        verbose_name_plural = "Прайс лист"


class Review(models.Model):
    """ Specialist review """
    specialist = models.ForeignKey(AUTH_USER_MODEL,
                                   related_name='reviews',
                                   on_delete=models.SET_NULL,
                                   null=True)
    text = models.CharField(max_length=500)
    data_updating = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL, blank=True, null=True, related_name="children"
    )
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.specialist} - {self.text} - {self.owner}"
