from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, CommentViewSet, FollowViewSet


router_v1 = DefaultRouter()

router_v1.register(r'posts', PostViewSet)
router_v1.register(r'posts\/(?P<post_pk>([1-9]\d*))\/comments\/(?P<comment_pk>([1-9]\d*))', CommentViewSet)
router_v1.register(r'follow', FollowViewSet)


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('auth/', include('djoser.urls.jwt')),
]
