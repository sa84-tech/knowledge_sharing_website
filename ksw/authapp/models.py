from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver



class WriterUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True)
    age = models.PositiveIntegerField(verbose_name='возраст', default=0)


class WriterUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'M'),
        (FEMALE, 'Ж'),
    )

    user = models.OneToOneField(WriterUser, unique=True, null=False, db_index=True, on_delete=models.CASCADE)

    gender = models.CharField(verbose_name='пол', max_length=1, choices=GENDER_CHOICES, blank=True)

    country = models.TextField(verbose_name='страна', max_length=35, blank=True)

    tagline = models.CharField(verbose_name='тэги', max_length=100, blank=True)

    about_me = models.TextField(verbose_name='о себе', max_length=150, blank=True)

    @receiver(post_save, sender=WriterUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            WriterUserProfile.objects.create(user=instance)

    @receiver(post_save, sender=WriterUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.writeruserprofile.save()
