from django.db import models
from django.contrib.auth.models import BaseUserManager
class UserProfileManager(BaseUserManager):
    def create_user(self,email,name,password=None):
        """
        Creates and saves a User with the given email,date of birth and password.
        :param email:
        :param name:
        :param password:
        :return:
        """
        if not email:
            raise ValueError('User must have an email address')
        user=self.model(
            email=self.normalize_email(email),
            name=name,
        )
        user.set_password(password)
        self.is_active=True
        user.save(using=self._db)
        return user
    def create_superuser(self,email,name,password):
        """
        Creates and saves a superuser with the given eamil,date of birth and password.
        :param email:
        :param name:
        :param password:
        :return:
        """
        user=self.create_user(
            email,
            password=password,
            name=name,

        )
        user.is_active=True
        user.is_admin=True
        user.save(using=self._db)
        return user