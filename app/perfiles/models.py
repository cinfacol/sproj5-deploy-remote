import os
import uuid
from pathlib import Path

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from djchoices import ChoiceItem, DjangoChoices
from djchoices.choices import ChoiceItem

BASE_DIR = Path(__file__).resolve().parent.parent


def user_directory_path_profile(instance, filename):
    profile_picture_name = 'users/{0}/profile.jpg'.format(
        instance.user.username)
    full_path = os.path.join(settings.MEDIA_ROOT, profile_picture_name)
    """ full_path = str(BASE_DIR.joinpath(
        settings.MEDIA_ROOT, profile_picture_name)) """

    if os.path.exists(full_path):
        os.remove(full_path)

    return profile_picture_name


def user_directory_path_banner(instance, filename):
    profile_picture_name = 'users/{0}/banner.jpg'.format(
        instance.user.username)
    full_path = os.path.join(settings.MEDIA_ROOT, profile_picture_name)
    """ full_path = str(BASE_DIR.joinpath(
        settings.MEDIA_ROOT, profile_picture_name)) """

    if os.path.exists(full_path):
        os.remove(full_path)

    return profile_picture_name


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, username, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username, password, **other_fields)

    def create_user(self, email, username, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username,
                          **other_fields)
        user.set_password(password)
        user.save()
        return user


class UserBase(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    # User Status
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"

    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            'l@1.com',
            [self.email],
            fail_silently=False,
        )

    def __str__(self):
        return self.username


class GenderType(DjangoChoices):
    male = ChoiceItem('male', 'Hombre')
    female = ChoiceItem('female', 'Mujer')


class VerificationType(DjangoChoices):
    unverified = ChoiceItem('unverified', 'No verificado')
    verified = ChoiceItem('verified', 'Verificado')


class Profile(models.Model):

    user = models.OneToOneField(
        UserBase, on_delete=models.CASCADE, related_name='profile')
    picture = models.ImageField(
        default='users/user_default_profile.png', upload_to=user_directory_path_profile)
    banner = models.ImageField(
        default='users/user_default_bg.jpg', upload_to=user_directory_path_banner)
    gender = models.CharField(
        max_length=10, choices=GenderType.choices, default=GenderType.male)
    verified = models.CharField(
        max_length=10, choices=VerificationType, default=VerificationType.unverified)
    url = models.CharField(max_length=80, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=150, null=True, blank=True)
    phone = models.CharField(max_length=50)
    mobile = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = 'Usuario'

    def __str__(self):
        return self.user.username


class AddressType(DjangoChoices):
    B = ChoiceItem('Billing')
    S = ChoiceItem('Shipping')


class Address(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserBase, on_delete=models.CASCADE)
    shipping_address = models.CharField(
        max_length=150, verbose_name='Dirección de envío')
    billing_address = models.CharField(
        max_length=150, verbose_name='Dirección de facturacion')
    pais = CountryField(multiple=False)
    departamento = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    zip = models.CharField(
        max_length=100, verbose_name='Zip code')
    address_type = models.CharField(
        max_length=8, choices=AddressType.choices, default=AddressType.S)
    default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.shipping_address}, {self.billing_address}, {self.ciudad}, {self.zip}"

    class Meta:
        verbose_name = 'Direccion'
        verbose_name_plural = 'Direcciones'


@receiver(post_save, sender=UserBase)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=UserBase)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
