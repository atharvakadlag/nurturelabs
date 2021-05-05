import uuid
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from datetime import datetime

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        """
        Create and return a `User` with an email, username and password.
        """
        if not email or not username:
            raise ValueError('Users Must Have an email address and username')
        print(f'Passvalue from create_user {password}')
        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    username = models.CharField(verbose_name='username', max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'password']

    objects = UserManager()

    def __str__(self):
        return f"{self.username} registered with {self.email}"

    class Meta:
        '''
        to set table name in database
        '''
        db_table = "user"

class Advisor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    advisor_name = models.CharField(max_length=255)
    advisor_profile_picture = models.ImageField(upload_to='images/')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"{self.advisor_name} advising {self.user}"

class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    time = models.DateTimeField(null=False)
    advisor = models.ForeignKey(Advisor, related_name='bookings',on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"{self.time} by {self.advisor}"