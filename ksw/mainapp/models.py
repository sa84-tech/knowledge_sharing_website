from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class Category(models.Model):
    name = models.CharField(
        verbose_name='имя категории',
        max_length=64,
        unique=True,
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

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
        User,
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
        User,
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
        verbose_name='количество просмотров'
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
        User,
        on_delete=models.CASCADE,
    )
    likes = GenericRelation(Like)
    comment = GenericRelation(Comment)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.topic

    @property
    def total_likes(self):
        return self.likes.count()

    @property
    def total_comment(self):
        return self.comment.count()

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-created']
