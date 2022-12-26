from django.db import models
from solo.models import SingletonModel
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from notes_site.managers import UserManager
from taggit.managers import TaggableManager
from uuid import uuid4


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True)
    first_name = models.CharField('first name', max_length=30, blank=True)
    last_name = models.CharField('last name', max_length=30, blank=True)
    date_joined = models.DateTimeField('date joined', auto_now_add=True)
    is_active = models.BooleanField('active', default=False)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email


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
        verbose_name = "Ркгистрация"
        verbose_name_plural = "Регистрации"


class Authorize(SingletonModel):
    description = models.TextField(
        verbose_name="Описание",
    )
    class Meta:
        db_table = "Authorize"
        verbose_name = "Авторизация"
        verbose_name_plural = "Авторизации"