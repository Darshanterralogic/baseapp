from django.urls import path,include
from . import views
from django.conf import settings

urlpatterns=[
    path('add_timeoff', views.add_timeoff, name='add_timeoff'),
    path('timeoff_list', views.timeoff_list, name='timeoff_list'),
    path('timeoff_delete/<int:id>', views.timeoff_delete, name='timeoff_delete'),
    path('timeoff_edit/<int:id>', views.timeoff_edit, name='timeoff_edit'),
]