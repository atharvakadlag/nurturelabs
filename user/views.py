from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from user.serializers import (
    UserSerializer, UserLoginSerializer, 
    AdminSerializer, AdvisorSerializer, BookingSerializer,
    AdvisorBookingSerializer, AllUsersRawSerializer
)
from user.models import User, Advisor, Booking

class UserView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_200_OK
        response = {
            'success' : 'True',
            'status code' : status_code,
            'message': 'User registered  successfully',
        }
        
        return Response(response, status=status_code)

class UserLoginView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def get(self, request):
        return Response({"No get allowed"})

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = { 
            'token' : serializer.data['token'],
            'user_id': serializer.data['user_id']
        }

        return Response(response)     

class AdminView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = AdminSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = {}

        return Response(response)

class AdvisorsView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = AdvisorSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Advisor.objects.filter(user__id=user_id)

class BookingCreateView(CreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = (AllowAny,)

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        if (advisor := self.kwargs['advisor_id']):
            draft_request_data = self.request.data.copy()
            draft_request_data['advisor'] = advisor
            kwargs['data'] = draft_request_data
            return serializer_class(*args, **kwargs)

        return serializer_class(*args, **kwargs)

    def post(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_200_OK
        response = {
            'success' : 'True',
            'status code' : status_code,
            'message': 'Booking created successfully',
        }

        return Response(response, status=status_code)

class AdvisorsBookingView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = AdvisorBookingSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Advisor.objects.filter(user__id=user_id)

class AllUsersRawView():
    permission_classes = (AllowAny,)
    serializer_class = AllUsersRawSerializer
    queryset = User.objects.all()