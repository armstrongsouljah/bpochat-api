import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    """
      This class handles the functionality of creating
      different user types.
    """
    def create_user(self, username, email, password=None):
        """
          This method creates a new user and saves it in the
          database.

          Args:
          username
          email
          password

          Returns:
           user object
        """
        if not username:
            raise TypeError("Username cannot be left blank")
        if not email:
            raise TypeError('Email cannot be blank')
        if not password:
            raise TypeError('Password cannot be blank')

        user = self.model(
            username=username,
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save()
        return user

    def create_staffuser(self, username, email, password=None):
        """
        This method creates  an user with access to the admin dashboard
        """
        user = self.create_user(
            username=username,
            email=email,
            password=password
        )
        if not password:
            raise TypeError('Password Cannot be left blank')
        user.is_staff = True
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        """
        This method creates an admin user with all rights.
        Args:
           username, email, password
        """
        if not password:
            raise TypeError('Password cannot be left blank')
        user = self.create_user(
            username,
            email,
            password
        )
        user.is_staff = True
        user.admin = True
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    """
      This structures data to be collected from the user
      as they attempt to register.
    """
    username = models.CharField(max_length=120)
    email = models.EmailField(max_length=255, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',  )
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    admin  = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)


    objects = UserManager()

    class Meta:
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.username}"

    def is_admin(self):
        return self.admin
    
    @property
    def get_fullname(self):
        return self.email

    def get_shortname(self):
        return self.username

    def is_active(self):
        return self.is_active

    def generate_jwt_token(self):
        
        token_str = str(self.email) + " " + str(self.username)
        token = jwt.encode(
            {
                'user_data': token_str,
                'exp': datetime.now() + timedelta(hours=3)
            }, settings.SECRET_KEY, algorithm='HS256'
        )
        return token.decode('utf-8')

    def token(self):
        """This method allows us to get users' token by calling 'user.token'"""
        return self.generate_jwt_token()

