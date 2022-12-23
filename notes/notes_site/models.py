from django.db import models
from django.contrib.auth.models import User
from solo.models import SingletonModel

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


class Hash(models.Model):
    user = models.OneToOneField(
        User,
        verbose_name="Хэш",
        on_delete=models.CASCADE,
    )
    hash_text = models.CharField(
        verbose_name="Тест хэша",
        max_length=64,
    )

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
