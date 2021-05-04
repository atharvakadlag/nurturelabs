from django.urls import path
from user.views import UserView, UserLoginView
from user.models import User
from user.serializers import UserSerializer


urlpatterns = [
    path('signup/', UserView.as_view()),
    path('signin/', UserLoginView.as_view())
]