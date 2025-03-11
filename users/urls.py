from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, UserDetailView, ProfileDetailView, ProfileListView

urlpatterns = [
    # Authentication
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User and Profile
    path('me/', UserDetailView.as_view(), name='user-detail'),
    path('profile/', ProfileDetailView.as_view(), name='profile-detail'),
    path('profiles/', ProfileListView.as_view(), name='profile-list'),
] 