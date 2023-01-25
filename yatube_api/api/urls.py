from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, CommentViewSet, FollowViewSet


router_v2 = DefaultRouter()

router_v2.register(r'posts', PostViewSet)
router_v2.register(r'posts\/(?P<post_pk>([1-9]\d*))\/comments', CommentViewSet)
router_v2.register(r'follow/', FollowViewSet)


urlpatterns = [
    path('v1/', include(router_v2.urls)),
    path('auth/', include('djoser.urls.jwt')),
]
