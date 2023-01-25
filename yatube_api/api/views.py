from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .serializers import PostSerializer, CommentSerializer, \
    FollowSerializer
from .permissions import AuthorPermission
from posts.models import Post, Comment, Follow


class MainViewSet(viewsets.ModelViewSet):
    '''Вьюсет для ограничения доступа к контенту, принадлежащего его автору.'''
    permission_classes = [AuthorPermission, IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostViewSet(MainViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


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


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
