from django.db import models
from django.utils import timezone

from .user import User


class Author(models.Model):
    """Модель автора"""

    author_id = models.AutoField(
        primary_key=True,
        verbose_name="ID"
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='author',
        null=True,
        blank=True,
    )
    name = models.CharField(
        verbose_name="Имя",
        max_length=150,
        null=False,
        blank=False
    )
    surname = models.CharField(
        verbose_name="Фамилия",
        max_length=150,
        null=False,
        blank=False
    )
    age = models.IntegerField(
        verbose_name="Возраст",
        null=False,
        blank=False,
        help_text="Возраст"
    )
    bio = models.TextField(
        verbose_name='Биография',
        null=True,
        blank=True,
    )
    date_joined = models.DateTimeField(
        verbose_name="Дата регистрации",
        default=timezone.now,
    )
    is_active = models.BooleanField(
        verbose_name="Активный",
        default=False
    )

    def get_date(self):
        return self.date_joined.strftime("%d.%m.%Y")

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
        ordering = ['-date_joined']

    def __str__(self) -> str:
        return f'{self.name} {self.surname}'
