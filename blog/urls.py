from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, LikeViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'likes', LikeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # Nested URLs for comments and likes on a specific post
    path('posts/<slug:post_slug>/comments/', CommentViewSet.as_view({'get': 'list', 'post': 'create'}), 
        name='post-comments'),
    path('posts/<slug:post_slug>/likes/', LikeViewSet.as_view({'get': 'list', 'post': 'create'}), 
        name='post-likes'),
] 