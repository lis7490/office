# employee/admin.py
from django.contrib import admin
from .models import Employee, Skill, EmployeeSkill, EmployeeImage

class EmployeeSkillInline(admin.TabularInline):
    model = EmployeeSkill
    extra = 1
    autocomplete_fields = ['skill']

class EmployeeImageInline(admin.TabularInline):
    model = EmployeeImage
    extra = 1
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image and obj.image.url:
            return f'<img src="{obj.image.url}" style="max-height: 100px;" />'
        return "Нет изображения"
    
    image_preview.allow_tags = True
    image_preview.short_description = 'Предпросмотр'

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = [
        'first_name', 
        'last_name', 
        'position', 
        'desk_number', 
        'hire_date', 
        'work_experience_days'
    ]
    
    list_filter = [
        'position', 
        'gender', 
        'hire_date'
    ]
    
    search_fields = [
        'first_name', 
        'last_name'
    ]
    
    # Убрали filter_horizontal для skills, так как используем промежуточную модель
    # Добавляем inline для навыков
    inlines = [
        EmployeeSkillInline,
        EmployeeImageInline
    ]
    
    fieldsets = (
        ('Основная информация', {
            'fields': (
                'first_name', 
                'last_name', 
                'gender', 
                'position'
            )
        }),
        ('Рабочее место', {
            'fields': (
                'desk_number', 
                'hire_date'
            )
        }),
        # Убрали раздел skills из fieldsets, так как используем inline
    )
    
    def work_experience_days(self, obj):
        return obj.get_work_experience_days()
    
    work_experience_days.short_description = 'Стаж (дни)'

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(EmployeeSkill)
class EmployeeSkillAdmin(admin.ModelAdmin):
    list_display = [
        'employee', 
        'skill', 
        'level_display'
    ]
    
    list_filter = [
        'level', 
        'skill'
    ]
    
    search_fields = [
        'employee__first_name', 
        'employee__last_name', 
        'skill__name'
    ]
    
    autocomplete_fields = ['employee', 'skill']
    
    def level_display(self, obj):
        return obj.get_level_display()
    
    level_display.short_description = 'Уровень'

@admin.register(EmployeeImage)
class EmployeeImageAdmin(admin.ModelAdmin):
    list_display = [
        'employee', 
        'image_preview_list',
        'uploaded_at'
    ]
    
    list_filter = [
        'uploaded_at'
    ]
    
    search_fields = [
        'employee__first_name', 
        'employee__last_name'
    ]
    
    ordering = ['employee', 'uploaded_at']
    
    readonly_fields = ['image_preview']
    
    def image_preview_list(self, obj):
        if obj.image and obj.image.url:
            return f'<img src="{obj.image.url}" style="max-height: 50px;" />'
        return "Нет изображения"
    
    image_preview_list.allow_tags = True
    image_preview_list.short_description = 'Предпросмотр'
    
    def image_preview(self, obj):
        if obj.image and obj.image.url:
            return f'<img src="{obj.image.url}" style="max-height: 200px;" />'
        return "Нет изображения"
    
    image_preview.allow_tags = True
    image_preview.short_description = 'Предпросмотр'