from app.admin.classes.models import Classes, DaysOfWeek


def get_days_of_week():
    days_of_week = DaysOfWeek.query.all()
    return days_of_week