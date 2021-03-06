from django.urls import path
from user.views import (
    UserView, UserLoginView, AdminView,
    AdvisorsView, BookingCreateView,
    AdvisorsBookingView
)
from user.models import User
from user.serializers import UserSerializer


urlpatterns = [
    path('user/register/', UserView.as_view()),
    path('user/login/', UserLoginView.as_view()),
    path('admin/advisor/', AdminView.as_view()),
    path('user/<uuid:user_id>/advisor/', AdvisorsView.as_view()),
    path('user/<uuid:user_id>/advisor/booking/', AdvisorsBookingView.as_view()),
    path('user/<uuid:user_id>/advisor/<uuid:advisor_id>/', BookingCreateView.as_view()),
]