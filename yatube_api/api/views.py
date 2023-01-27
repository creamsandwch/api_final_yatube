from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly,\
    IsAuthenticated

from .serializers import PostSerializer, CommentSerializer, \
    FollowSerializer, GroupSerializer
from .permissions import AuthorPermission
from posts.models import Post, Comment, Follow, Group


class MainViewSet(viewsets.ModelViewSet):
    '''Вьюсет для ограничения доступа к контенту, принадлежащего его автору.'''
    permission_classes = [AuthorPermission, IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ListRetrieveViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = [IsAuthenticatedOrReadOnly]


class PostViewSet(MainViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination


class CommentViewSet(MainViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        post_instance = get_object_or_404(Post, id=self.kwargs.get('post_pk'))
        serializer.save(
            author=self.request.user,
            post=post_instance
        )

    def get_queryset(self):
        post_pk = self.kwargs.get('post_pk')
        post = get_object_or_404(Post, id=post_pk)
        return post.comments.all()


class FollowViewSet(MainViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = (filters.SearchFilter,)
    search_fields = ('user__username', 'following__username')

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )
        return super().perform_create(serializer)

    def get_queryset(self):
        queryset = Follow.objects.filter(user=self.request.user)
        return queryset


class GroupViewSet(ListRetrieveViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
