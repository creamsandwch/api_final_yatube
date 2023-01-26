from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, CommentViewSet, FollowViewSet, GroupViewSet


router_v1 = DefaultRouter()

router_v1.register(r'posts', PostViewSet)
router_v1.register(r'posts\/(?P<post_pk>([1-9]\d*))\/comments', CommentViewSet)
router_v1.register(r'follow', FollowViewSet)
router_v1.register(r'groups', GroupViewSet)


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
