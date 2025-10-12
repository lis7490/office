from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Employee, EmployeeImage  # Добавьте этот импорт
# Create your views here.
def home(request):
    return HttpResponse('Главная страница')

def one(request):
    return HttpResponse('Cтраница №1')




# Список всех сотрудников
class EmployeeListView(ListView):
    model = Employee
    template_name = 'employee/employee_list.html'
    context_object_name = 'employees'
    paginate_by = 10

    def get_queryset(self):
        return Employee.objects.prefetch_related('images').all()

# Детальная страница сотрудника
class EmployeeDetailView(DetailView):
    model = Employee
    template_name = 'employee/employee_detail.html'
    context_object_name = 'employee'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем упорядоченные изображения в контекст
        context['images'] = self.object.get_ordered_images()
        return context

# Создание нового сотрудника
class EmployeeCreateView(CreateView):
    model = Employee
    template_name = 'employee/employee_form.html'
    fields = ['name', 'gender', 'skills', 'level_skills', 'description', 'workplace']
    success_url = reverse_lazy('employee_list')

# Редактирование сотрудника
class EmployeeUpdateView(UpdateView):
    model = Employee
    template_name = 'employee/employee_form.html'
    fields = ['name', 'gender', 'skills', 'level_skills', 'description', 'workplace']
    success_url = reverse_lazy('employee_list')

# Удаление сотрудника
class EmployeeDeleteView(DeleteView):
    model = Employee
    template_name = 'employee/employee_confirm_delete.html'
    success_url = reverse_lazy('employee_list')

# Функциональные представления (если нужны)
def employee_search(request):
    query = request.GET.get('q', '')
    employees = Employee.objects.filter(name__icontains=query) if query else Employee.objects.none()
    return render(request, 'employee/employee_search.html', {
        'employees': employees,
        'query': query
    })

# Представление для галереи изображений сотрудника
def employee_gallery(request, pk):
    employee = Employee.objects.get(pk=pk)
    images = employee.get_ordered_images()
    return render(request, 'employee/employee_gallery.html', {
        'employee': employee,
        'images': images
    })




