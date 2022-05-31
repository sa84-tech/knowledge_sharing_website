from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.shortcuts import reverse
from ckeditor_uploader.fields import RichTextUploadingField

from accountapp.models import Bookmark
from .services.images import crop_rect
from .services.notifications import post_signal_handler, comment_signal_handler

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
        unique_together = ('content_type', 'object_id', 'author')
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'


class View(models.Model):
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
        unique_together = ('content_type', 'object_id', 'author')
        verbose_name = 'Количество Просмотров'


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name="comments")
    body = models.TextField(
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

    comments = GenericRelation('self')
    like = GenericRelation(Like)
    bookmark = GenericRelation(Bookmark)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def total_likes(self):
        return self.like.count()

    @property
    def total_bookmarks(self):
        return self.bookmark.count()

    def get_comments(self):
        return self.comments.all()

    def _get_content_obj(self, content_obj_name: str):
        content_objects = {
            'like': self.like,
            'bookmark': self.bookmark,
        }

        if content_objects[content_obj_name]:
            return content_objects[content_obj_name]
        return None

    def has_relation_with(self, user, content_obj_name: str) -> bool:
        """ Проверяет, есть ли у 'user' один из 'content_obj' для статьи
        :parm content_obj_name: view, like, comment, bookmark
        """
        content_obj = self._get_content_obj(content_obj_name)
        if user.is_authenticated and content_obj:
            related_objects = content_obj.filter(object_id=self.pk,
                                                 author_id=user.pk,
                                                 content_type=ContentType.objects.get_for_model(self))
            return related_objects.exists()
        return False

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
    like = GenericRelation(Like)
    comment = GenericRelation(Comment)
    bookmark = GenericRelation(Bookmark)
    view = GenericRelation(View)
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
        return self.like.count()

    @property
    def total_comments(self):
        return self.comments.count()

    @property
    def total_bookmarks(self):
        return self.bookmark.count()

    @property
    def total_views(self):
        return self.view.count()

    def _get_content_obj(self, content_obj_name: str):
        content_objects = {
            'view': self.view,
            'comment': self.comment,
            'like': self.like,
            'bookmark': self.bookmark,
        }

        if content_objects[content_obj_name]:
            return content_objects[content_obj_name]
        return None

    def has_relation_with(self, user, content_obj_name: str) -> bool:
        """ Проверяет, есть ли у 'user' один из 'content_obj' для статьи
        :parm content_obj_name: view, like, comment, bookmark
        """
        content_obj = self._get_content_obj(content_obj_name)
        if user.is_authenticated and content_obj:
            if content_obj_name == 'comment':
                related_objects = self.comments.filter(author=user)
            else:
                related_objects = content_obj.filter(object_id=self.pk,
                                                     author_id=user.pk,
                                                     content_type=ContentType.objects.get_for_model(self))
            return related_objects.exists()
        return False

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-created']


post_save.connect(post_signal_handler, sender=Post)
post_save.connect(comment_signal_handler, sender=Comment)
