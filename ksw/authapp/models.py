from datetime import timedelta, datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from django_countries.fields import CountryField

# from mainapp.models import Like, Comment, Post
from mainapp.services.images import crop_square
# from authapp.services.queries import get_user_rating, get_user_activity

AVATAR_SIZE = 200


class WriterUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True)
    email = models.EmailField(verbose_name='email', blank=False, unique=True)
    birthday = models.DateField(blank=True, null=True)

    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=(now() + timedelta(hours=48)))

    def is_activation_key_expired(self):
        if now() <= self.activation_key_expires:
            return False
        else:
            return True

    def save(self, *args, **kwargs):
        super().save()
        if self.avatar:
            img = crop_square(self.avatar.path, AVATAR_SIZE)
            img.save(self.avatar.path, 'png')

    @property
    def full_name(self):
        return self.get_full_name()

    @property
    def status(self):
        if self.is_superuser:
            return 'суперпользователь'
        if self.is_staff:
            return 'модератор'
        return 'пользователь'


class WriterUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'Mужчина'),
        (FEMALE, 'Женщина'),
    )

    user = models.OneToOneField(WriterUser, unique=True, null=False, db_index=True, on_delete=models.CASCADE)

    gender = models.CharField(verbose_name='пол', max_length=7, choices=GENDER_CHOICES, blank=True)

    country = CountryField(blank=True)

    tagline = models.CharField(verbose_name='тэги', max_length=100, blank=True)

    about_me = models.TextField(verbose_name='о себе', max_length=150, blank=True)

    @receiver(post_save, sender=WriterUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            WriterUserProfile.objects.create(user=instance)

    @receiver(post_save, sender=WriterUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.writeruserprofile.save()
