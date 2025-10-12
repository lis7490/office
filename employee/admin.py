from django.contrib import admin
from django.utils.html import format_html
from .models import Employee, EmployeeImage

class EmployeeImageInline(admin.TabularInline):
    model = EmployeeImage
    extra = 1
    fields = ('image', 'image_preview', 'title', 'order')
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="100" height="100" style="object-fit: cover;" />',
                obj.image.url
            )
        return "Нет изображения"
    image_preview.short_description = 'Предпросмотр'

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'position_display', 'workplace', 'images_count')
    list_filter = ('gender', 'workplace')
    search_fields = ('name', 'skills')
    inlines = [EmployeeImageInline]
    
    def position_display(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    position_display.short_description = 'Должность'
    
    def images_count(self, obj):
        return obj.images_count()
    images_count.short_description = 'Фото'

@admin.register(EmployeeImage)
class EmployeeImageAdmin(admin.ModelAdmin):
    list_display = ('employee', 'order', 'title', 'image_preview', 'created_at')
    list_filter = ('employee',)
    list_editable = ('order', 'title')
    search_fields = ('employee__name', 'title')
    ordering = ('employee', 'order')
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover;" />',
                obj.image.url
            )
        return "Нет изображения"
    image_preview.short_description = 'Предпросмотр'