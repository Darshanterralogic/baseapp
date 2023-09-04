from django.urls import path,include
from . import views
from django.conf import settings

urlpatterns=[
    path('add_timesheet', views.add_timesheet, name='add_timesheet'),
    path('timesheet_list', views.timesheet_list, name='timesheet_list'),
    path('timesheet_delete/<int:id>', views.timesheet_delete, name='timesheet_delete'),
    path('timesheet_edit/<int:id>', views.timesheet_edit, name='timesheet_edit'),
]