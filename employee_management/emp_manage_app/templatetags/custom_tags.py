from django.template import Library
from employee_management.emp_manage_app.models import EmployeeSchedule
from datetime import datetime

register = Library()

@register.simple_tag(name='get_latest_sch')
def get_latest_sch(user_id, shift):
    most_upcoming = EmployeeSchedule.objects.filter(employee_id=user_id).order_by('-shift_start')
    if most_upcoming:
        if shift == 'start':
            schedule_shift_start = datetime.strftime(most_upcoming[0].shift_start, '%b %d %Y  %I:%M')
            return schedule_shift_start
        else:
            schedule_shift_end = datetime.strftime(most_upcoming[0].shift_ends, '%b %d %Y  %I:%M')
            return schedule_shift_end

    else:
        return None

