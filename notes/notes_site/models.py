from django.db import models
from solo.models import SingletonModel
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractUser
from notes_site.managers import UserManager
from taggit.managers import TaggableManager
from uuid import uuid4


class User(AbstractUser, PermissionsMixin):

    objects = UserManager()

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'



class Note(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        verbose_name="Заголовок",
        max_length=64,
    )
    description = models.TextField(
        verbose_name="Описание",
    )

    posted_date = models.DateTimeField(
        verbose_name="Дата публикации",
        auto_now_add=True,
    )

    tags = TaggableManager()

    def __str__(self):
        return self.title

    class Meta:
        db_table = "notes"
        verbose_name = "Заметка"
        verbose_name_plural = "Заметки"




class EmailHash(models.Model):
    user = models.OneToOneField(
        User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
    )
    hash_text = models.CharField(
        verbose_name="Хэш",
        max_length=64,
        default=uuid4
    )

    def __str__(self):
        return self.user.email

    class Meta:
        db_table = "hash"
        verbose_name = "Hash"
        verbose_name_plural = "Hashs"


class Registration(SingletonModel):
    description = models.TextField(
        verbose_name="Описание",
    )
    class Meta:
        db_table = "Registration"
        verbose_name = "Регистрация"
        verbose_name_plural = "Регистрации"


class Authorize(SingletonModel):
    description = models.TextField(
        verbose_name="Описание",
    )
    class Meta:
        db_table = "Authorize"
        verbose_name = "Авторизация"
        verbose_name_plural = "Авторизации"


class MailSettings(SingletonModel):
    domen = models.CharField(
        max_length = 64,
        verbose_name = "Домен",
    )
    title = models.CharField(
        max_length = 128,
        verbose_name = "Заголовок",
    )
    description = models.TextField(
        verbose_name = "Описание"
    )
    class Meta:
        db_table = "mail_setinngs"
        verbose_name = "Настройки почты"
        verbose_name_plural = "Настройки почт"

