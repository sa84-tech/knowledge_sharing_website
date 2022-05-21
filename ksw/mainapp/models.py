from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from ckeditor_uploader.fields import RichTextUploadingField

from .services.helpers import get_cti
from .services.images import crop_rect
from accountapp.models import Bookmark


WIDTH_TO_HEIGHT_RATIO = 0.72


class Category(models.Model):
    name = models.CharField(
        verbose_name='имя категории',
        max_length=64,
        unique=True,
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name="URL-slug",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('index_page', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class StatusArticle(models.Model):
    name = models.CharField(
        verbose_name='название статуса',
        max_length=64,
        unique=True,
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class Like(models.Model):
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )

    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'


class Comment(models.Model):
    comment = models.TextField(
        verbose_name='комментарий',
        max_length=250,
    )

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )

    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'


class Post(models.Model):
    topic = models.CharField(
        verbose_name='название статьи',
        max_length=200,
    )

    annotation = RichTextUploadingField(
        verbose_name='анотация',
        max_length=256,
        blank=True,
        null=True,
    )

    article = RichTextUploadingField(
        verbose_name='текст статьи',
        blank=True,
        null=True,
    )

    total_views = models.PositiveIntegerField(
        verbose_name='количество просмотров',
        default=0
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='категория',
    )

    status = models.ForeignKey(
        StatusArticle,
        on_delete=models.CASCADE,
        verbose_name='статус',
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    likes = GenericRelation(Like)
    comment = GenericRelation(Comment)
    bookmark = GenericRelation(Bookmark)
    image = models.ImageField(upload_to='uploads/%Y/%m/%d', blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.topic

    def save(self, *args, **kwargs):
        super().save()
        if self.image:
            img = crop_rect(self.image.path, WIDTH_TO_HEIGHT_RATIO)
            img.save(self.image.path, 'png')

    @property
    def total_likes(self):
        return self.likes.count()

    @property
    def total_comments(self):
        return self.comment.count()

    @property
    def total_bookmarks(self):
        return self.bookmark.count()

    def is_liked_by(self, user):
        if user.is_authenticated:
            return self.likes.filter(object_id=self.pk,
                                     author_id=user.pk,
                                     content_type_id=get_cti('post')).exists()

        return False

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-created']
