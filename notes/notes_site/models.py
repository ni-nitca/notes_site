from django.db import models
from solo.models import SingletonModel
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractUser
from notes_site.managers import UserManager
from uuid import uuid4
from django.shortcuts import reverse


class User(AbstractUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True)
    username = None
    is_active = models.BooleanField('active', default=False)

    objects = UserManager()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    class Meta:
        db_table = "users"
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


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
    slug = models.SlugField(
        max_length=64,
        unique=True,
        verbose_name="URL"
    )

    posted_date = models.DateTimeField(
        verbose_name="Дата публикации",
        auto_now_add=True,
    )

    def get_remove_url(self):#подумать над тем как вернуть на главную
        return f"/note/{self.slug}"

    def get_edit_url(self):
        return f"/note/{self.slug}"

    def get_absolute_url(self):
        return reverse("note-create", kwargs={"slug": self.slug})

    def __str__(self):
        return str(self.title)

    class Meta:
        db_table = "notes"
        verbose_name = "Заметка"
        verbose_name_plural = "Заметки"


class Tags(models.Model):
    tags = models.ForeignKey(
        Note,
        verbose_name="Заметка",
        on_delete=models.CASCADE,
    )
    tag = models.CharField(
        verbose_name="Тег",
        max_length=64,
    )

    def __str__(self):
        return str(self.tag)

    class Meta:
        db_table = "tags"
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


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
        return str(self.hash_text)

    class Meta:
        db_table = "hash"
        verbose_name = "Hash"
        verbose_name_plural = "Hashs"


class Registration(SingletonModel):
    description = models.TextField(
        verbose_name="Описание",
        default="Заполните поля ниже"
    )
    class Meta:
        db_table = "Registration"
        verbose_name = "Регистрация"
        verbose_name_plural = "Регистрации"


class Authorize(SingletonModel):
    description = models.TextField(
        verbose_name="Описание",
        default="Приглашаем вас авторизоваться для просмотра заметок"
    )
    class Meta:
        db_table = "Authorize"
        verbose_name = "Авторизация"
        verbose_name_plural = "Авторизации"


class MailSettings(SingletonModel):
    domen = models.CharField(
        max_length = 64,
        verbose_name = "Домен",
        default = "127.0.0.0.1:8000"
    )
    title = models.CharField(
        max_length = 128,
        verbose_name = "Заголовок",
        default = "Актвация аккаунта"
    )
    description = models.TextField(
        verbose_name = "Описание",
        default = "Активация аккаунта"
    )
    class Meta:
        db_table = "mail_setinngs"
        verbose_name = "Настройки почты"
        verbose_name_plural = "Настройки почт"
