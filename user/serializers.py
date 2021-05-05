from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.contrib.auth.hashers import make_password
from django.utils.encoding import force_text
from rest_framework import serializers, status
from rest_framework_jwt.settings import api_settings
from rest_framework.exceptions import APIException
from user.models import User, Advisor, Booking

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class ValidationError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'A server error occurred.'

    def __init__(self, detail, status_code, field = None):
        if status_code is not None:
            self.status_code = status_code

        if detail is not None:
            self.detail = {field: force_text(detail)}
        else: 
            self.detail = {'detail': force_text(self.default_detail)}

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password':{
                'write_only':True,
                'style': {'input_type': 'password'}
            }
        }
    def validate_password(self, value: str) -> str:
        return make_password(value)

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    user_id = serializers.UUIDField(read_only=True)

    def validate(self, data):
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)
        if user is None:
            raise ValidationError(
                detail = 'Incorrect username or password',
                status_code = status.HTTP_401_UNAUTHORIZED
            )
        
        payload = JWT_PAYLOAD_HANDLER(user)
        jwt_token = JWT_ENCODE_HANDLER(payload)
        update_last_login(None, user)

        return {
            'username': user.username,
            'token': jwt_token,
            'user_id': user.id
        }

class AdminSerializer(serializers.Serializer):
    advisor_name = serializers.CharField(max_length=255)
    advisor_img_url = serializers.URLField(max_length=511)
     
    def validate(self, data):
        advisor_name = data['advisor_name']
        advisor_img_url = data['advisor_img_url']

        return {
            'advisor_name': advisor_name,
            'advisor_img_url': advisor_img_url
        }

class AdvisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advisor
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

class AdvisorBookingSerializer(serializers.ModelSerializer):
    bookings = BookingSerializer(many=True, read_only=True)

    class Meta:
        model = Advisor
        fields = '__all__'

class AllUsersRawSerializer():
    class Meta:
        model = User
        fields = '__all__'