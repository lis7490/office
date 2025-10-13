
from django.urls import path
from .import views
from .views import EmployeeListView, EmployeeDetailView

app_name = 'employee'

urlpatterns = [
    path('', views.home, name='home'),
    path('1/', views.one),
    path('users', EmployeeListView.as_view(), name='employee_list'),
    path('employee/<int:pk>/', EmployeeDetailView.as_view(), name='employee_detail')
]