from django.db import models
from workplace.models import Workplace
from django.core.exceptions import ValidationError
import os

from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

class Employee(models.Model):
    GENDER_CHOICES = [
        ("M", "Мужской"),
        ("F", "Женский")  # Исправлено: "F" вместо "Ж" для consistency
    ]
    
    gender = models.CharField(
        max_length=1,  # Уменьшено т.к. один символ
        choices=GENDER_CHOICES,
        verbose_name="Пол"
    )
    name = models.CharField(max_length=100, verbose_name="ФИО")
    skills = models.CharField(
        max_length=250,
        verbose_name="Навыки",
        help_text="Перечислите навыки через запятую",
    )
    level_skills = models.CharField(  # Исправлена опечатка: level_sills -> level_skills
        max_length=250, 
        verbose_name="Уровень навыков", 
        help_text="от 1 до 10"
    )
    description = models.TextField(  # Изменено на TextField для более длинных описаний
        max_length=500, 
        verbose_name="Описание",
        blank=True  # Сделано необязательным
    )

    workplace = models.OneToOneField(
        Workplace,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Рабочее место",
        related_name="employee",
    )

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        ordering = ['name']  # Добавлена сортировка по умолчанию

    def __str__(self):
        return self.name
    
    @property
    def main_image(self):
        """Возвращает первое изображение из галереи"""
        return self.images.first()
    
    def get_ordered_images(self):
        """Возвращает изображения в правильном порядке"""
        return self.images.all().order_by('order')
    
    def images_count(self):
        """Количество изображений у сотрудника"""
        return self.images.count()
    
    def get_skills_list(self):
        """Возвращает список навыков"""
        return [skill.strip() for skill in self.skills.split(',') if skill.strip()]


class EmployeeImage(models.Model):
    employee = models.ForeignKey(
        Employee,  # Убраны кавычки т.к. класс определен выше
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Сотрудник'
    )
    image = models.ImageField(
        upload_to='employees/gallery/%Y/%m/%d/',  # Добавлена структура папок по дате
        verbose_name='Изображение'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядковый номер',
        help_text='Чем меньше число, тем выше в списке'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
    )
    title = models.CharField(  # Добавлено поле для названия/описания изображения
        max_length=200,
        verbose_name='Название изображения',
        blank=True,
        help_text='Необязательное описание изображения'
    )

    class Meta:
        verbose_name = 'Изображение сотрудника'
        verbose_name_plural = 'Изображения сотрудников'
        ordering = ['order', 'created_at']
        unique_together = ['employee', 'order']
    
    def __str__(self):
        title = self.title or f"Изображение {self.order}"
        return f"{title} для {self.employee.name}"
    
    def clean(self):
        """Валидация данных"""
        if self.order < 0:
            raise ValidationError({'order': 'Порядковый номер не может быть отрицательным'})
    
    def save(self, *args, **kwargs):
        """Автоматическая установка порядка если не указан"""
        if self.pk is None and self.order == 0:  # Только для новых объектов
            max_order = EmployeeImage.objects.filter(
                employee=self.employee
            ).aggregate(models.Max('order'))['order__max'] or 0
            self.order = max_order + 1
        
        super().save(*args, **kwargs)
    
    def filename(self):
        """Возвращает имя файла"""
        return os.path.basename(self.image.name)
    
    def get_image_url(self):
        """Возвращает URL изображения"""
        if self.image:
            return self.image.url
        return None
    
@receiver(post_delete, sender=EmployeeImage)
def reorder_images_after_delete(sender, instance, **kwargs):
    """Пересчет порядка после удаления изображения"""
    # Получаем все изображения сотрудника, отсортированные по порядку
    remaining_images = EmployeeImage.objects.filter(
        employee=instance.employee
    ).order_by('order', 'created_at')
    
    # Перенумеровываем оставшиеся изображения
    for index, image in enumerate(remaining_images, 1):
        if image.order != index:
            image.order = index
            image.save()

@receiver(pre_save, sender=EmployeeImage)
def validate_unique_order(sender, instance, **kwargs):
    """Проверка уникальности порядка перед сохранением"""
    if instance.order != 0:  # Если порядок указан явно
        existing = EmployeeImage.objects.filter(
            employee=instance.employee,
            order=instance.order
        ).exclude(pk=instance.pk)  # Исключаем текущий объект при обновлении
        
        if existing.exists():
            # Находим свободный порядковый номер
            max_order = EmployeeImage.objects.filter(
                employee=instance.employee
            ).aggregate(models.Max('order'))['order__max'] or 0
            instance.order = max_order + 1