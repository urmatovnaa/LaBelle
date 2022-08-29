from django.contrib import admin
from django.contrib.admin.options import TabularInline

from wall_app.models import Post, PriceList, Review, Image, Comment


class PostImageAdminInline(TabularInline):
    extra = 1
    model = Image
    max_num = 10


@admin.register(Post)
class RestaurantModelAdmin(admin.ModelAdmin):
    inlines = (PostImageAdminInline,)
    # readonly_fields = ['id']


admin.site.register(PriceList)
admin.site.register(Review)
admin.site.register(Comment)
