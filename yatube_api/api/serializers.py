import base64

from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator, \
    UniqueValidator


from posts.models import Comment, Post, Follow, Group


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(
                base64.b64decode(imgstr),
                name='temp' + ext
            )
        return super().to_internal_value(data=data)


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )
    image = Base64ImageField(allow_null=True)

    class Meta:
        fields = (
            'id',
            'author',
            'text',
            'pub_date',
            'image',
            'group',
        )
        model = Post
        required_fields = ('text',)


class GroupSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        validators=[UniqueValidator(queryset=Group.objects.all())],
        read_only=True
    )

    class Meta:
        model = Group
        fields = (
            'id',
            'title',
            'slug',
            'description',
        )
        required_fields = ('title', )
        read_only_fields = ('title', 'slug', 'description')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True, slug_field='username'
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = (
            'id',
            'author',
            'text',
            'created',
            'post',
        )
        model = Comment
        required_fields = ('text', )


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True,
    )
    following = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True,
    )

    class Meta:
        fields = ('user', 'following')
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message='Объект подписки уже существует!',
            )
        ]
        required_fields = ('user', 'following')
