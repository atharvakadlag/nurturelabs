from django.urls import path
from user.views import UserView, UserLoginView, AdminView
from user.models import User
from user.serializers import UserSerializer


urlpatterns = [
    path('user/register/', UserView.as_view()),
    path('user/login/', UserLoginView.as_view()),
    path('admin/advisor/', AdminView.as_view())
]