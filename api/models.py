from __future__ import unicode_literals
from django.db import models

# Create your models here.

from django.contrib.auth.models import (
        AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
import jwt

from datetime import datetime, timedelta

from django.conf import settings


#Creation du model User pour les utilisateurs de l'application pour securiser l'entree des commandes

class UserManager(BaseUserManager):
    def create_user(self, username, email,password, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('users must have an email address')
        if not username:
            raise ValueError('Username is required.')
        if password is None:
            raise TypeError('User must have a password.')
        user = self.model(username=username, email=self.normalize_email(email),**extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password, **extra_fields):

    #    Create and save a SuperUser with the given email and password.

            extra_fields.setdefault('is_staff', True)
            extra_fields.setdefault('is_superuser', True)
            extra_fields.setdefault('is_active', True)

            if extra_fields.get('is_staff') is not True:
                raise ValueError(_('Superuser must have is_staff=True.'))
            if extra_fields.get('is_superuser') is not True:
                raise ValueError(_('Superuser must have is_superuser=True.'))
            return self.create_user(email,username, password, **extra_fields)


class CustomUser(AbstractBaseUser,PermissionsMixin):
    """My own custom user class"""
    first_name = models.CharField(max_length = 100, verbose_name =_('first name'))
    last_name = models.CharField(max_length = 100, verbose_name =_('last name'))
    username = models.CharField(max_length = 100, unique = True, verbose_name =_('username'))
    email = models.EmailField(max_length=255, unique=True, db_index=True, verbose_name=_('email address'))
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email';'username'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        """
        Returns a string representation of this `User`.

        This string is used when a `User` is printed in the console.
        """
        return self.username
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().

        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        return self._generate_jwt_token()

    def get_full_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically this would be the user's first and last name. Since we do
        not store the user's real name, we return their username instead.
        """
        return self.first_name

    def get_short_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically, this would be the user's first name. Since we do not store
        the user's real name, we return their username instead.
        """
        return self.username

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 360 days into the future.
        """
        dt = datetime.now() + timedelta(days=360)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')



class Lunette (models.Model):
    name = models.CharField(max_length = 30, blank = False, null = False)
    type = models.TextField(max_length = 100, blank = False, null = True)
    price = models.IntegerField(null = False)
    photo = models.ImageField(upload_to = 'photoLunette')

    def __str__(self):
        return str(self.name) + '  '


class Client(models.Model):
    lastname = models.CharField(max_length = 30, blank = False, null = False)
    firstname = models.CharField(max_length = 30, blank = False, null = False)
    adress = models.TextField(max_length = 100, blank = False, null = True)
    phone = models.IntegerField(null = False)
    photo = models.ImageField(upload_to = 'photoClient')

    def __str__(self):
        return str(self.firstname) + '  '


class Commande(models.Model):
    client = models.ForeignKey('Client', on_delete = models.CASCADE, null = False, blank = True )
    lunette = models.ForeignKey('Lunette', on_delete = models.CASCADE, null = False, blank = True )
    user = models.ForeignKey('CustomUser', on_delete = models.CASCADE, null = False, blank = True ) #connaitre ll'utilisateur qui a passe la commande
    date = models.DateField(null = False)
    nbre_lunettes = models.IntegerField(null = False)
    montant_total = models.IntegerField(null = False)

    def __str__(self):
        return str(self.client) + '  '
