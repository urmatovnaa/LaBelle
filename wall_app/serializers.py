from rest_framework import serializers

from wall_app.models import Image, Comment, PriceList, Post, Review


class FilterParentSerializer(serializers.ListSerializer):
    """Фильтр комментариев/отзывов, только parents"""
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    """Вывод рекурсивно children"""
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = '__all__'


class CommentCreateSerializer(serializers.ModelSerializer):
    """Добавление комментария"""

    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
            'post': {'read_only': True}
        }


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Добавление отзыва"""

    class Meta:
        model = Review
        fields = '__all__'
        extra_kwargs = {
            'owner': {'read_only': True},
            'specialist': {'read_only': True}
        }


class ReviewSerializer(serializers.ModelSerializer):
    """Вывод отзыва"""
    username = serializers.CharField(read_only=True)
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterParentSerializer
        model = Review
        fields = ("id", "username", "text", "children", 'user', 'post', 'data_updating')
        extra_kwargs = {
            'owner': {'read_only': True},
            'specialist': {'read_only': True}
        }


class CommentSerializer(serializers.ModelSerializer):
    """Вывод коммента"""
    username = serializers.CharField(read_only=True)
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterParentSerializer
        model = Comment
        fields = ("id", "username", "text", "children", "user", 'post', 'data_creating')
        extra_kwargs = {
            'user': {'read_only': True},
            'post': {'read_only': True}
        }


class PriceListSerializer(serializers.ModelSerializer):
    """Добавление и вывод прайса """

    class Meta:
        model = PriceList
        fields = '__all__'
        extra_kwargs = {
            'specialist': {'read_only': True},
        }


class PostDetailSerializer(serializers.ModelSerializer):
    """Детальный пост"""
    owner_name = serializers.CharField(read_only=True)
    image = ImageSerializer(many=True)
    likes_count = serializers.IntegerField()
    comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = (
            'id', 'data_creating', 'description', 'owner', 'tags',
            'image', 'owner_name', 'comments', 'likes_count'
        )
        extra_kwargs = {'user': {'read_only': True}}



