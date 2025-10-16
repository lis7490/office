from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class NeighborDeskValidator:
    """
    Валидатор, запрещающий тестировщикам и разработчикам 
    занимать соседние столы
    """
    
    def are_neighbors(self, desk1, desk2):
        """
        Проверяет, являются ли столы соседними
        """
        if not desk1 or not desk2:
            return False
            
        # Простая логика: столы с последовательными номерами - соседи
        try:
            num1 = desk1.number
            num2 = desk2.number
            if len(num1) == len(num2) and num1[:-1] == num2[:-1]:
                return abs(int(num1[-1]) - int(num2[-1])) == 1
        except (ValueError, IndexError, AttributeError):
            pass
        
        # Логика с координатами
        if hasattr(desk1, 'coordinates_x') and hasattr(desk2, 'coordinates_x'):
            return (abs(desk1.coordinates_x - desk2.coordinates_x) <= 1 and 
                    abs(desk1.coordinates_y - desk2.coordinates_y) <= 1)
        
        return False
    
    def validate(self, reservation):
        """Основной метод валидации"""
        # Импортируем модель здесь, чтобы избежать циклического импорта
        from .models import Reservation as ReservationModel
        
        # Пропускаем валидацию если нет даты или стола
        if not reservation.date or not reservation.desk:
            return
            
        # Получаем все резервации на эту дату
        same_date_reservations = ReservationModel.objects.filter(
            date=reservation.date
        ).exclude(id=reservation.id if reservation.id else None)
        
        for existing_reservation in same_date_reservations:
            if self.are_neighbors(reservation.desk, existing_reservation.desk):
                # Проверяем роли пользователей
                if (self.is_tester(reservation.user) and 
                    self.is_developer(existing_reservation.user)) or \
                   (self.is_developer(reservation.user) and 
                    self.is_tester(existing_reservation.user)):
                    raise ValidationError(
                        _('Тестировщики и разработчики не могут занимать соседние столы'),
                        code='neighbor_desk_conflict'
                    )
    
    def is_tester(self, user):
        """Проверяет, является ли пользователь тестировщиком"""
        return user.groups.filter(name='Testers').exists()
    
    def is_developer(self, user):
        """Проверяет, является ли пользователь разработчиком"""
        return user.groups.filter(name='Developers').exists()