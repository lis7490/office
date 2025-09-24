from django.db import models
from workplace.models import Workplace


class Employee(models.Model):

    GENDER_CHOICES = [("M", "Мужской"), ("Ж", "Женский")]
    gender = models.CharField(max_length=20, verbose_name="Пол")
    name = models.CharField(max_length=100, verbose_name="ФИО")
    skills = models.CharField(
        max_length=250,
        verbose_name="Навыки",
        help_text="Перечислите навыки через запятую",
    )
    level_sills = models.CharField(
        max_length=250, verbose_name="Уровень навыков", help_text="от 1 до 10"
    )
    description = models.CharField(max_length=250, verbose_name="Описание")

    workplace = models.OneToOneField(
        Workplace,
        on_delete=models.SET_NULL,  # или models.PROTECT, models.CASCADE
        null=True,
        blank=True,
        verbose_name="Рабочее место",
        related_name="employee",  # Обратная связь
    )

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return self.name


# Create your models here.
