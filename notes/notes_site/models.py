from django.db import models
from solo.models import SingletonModel
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from taggit.managers import TaggableManager


class Note(models.Model):
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


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


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
        return self.user.email


class EmailHash(models.Model):
    user = models.OneToOneField(
        User,
        verbose_name="Хэш",
        on_delete=models.CASCADE,
    )
    hash_text = models.CharField(
        verbose_name="Тест хэша",
        max_length=64,
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


class Authorize(SingletonModel):
    description = models.TextField(
        verbose_name="Описание",
    )
