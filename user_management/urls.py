from django.urls import path,include
from . import views
from django.conf import settings

urlpatterns=[

    path('', views.signin, name='signin'),
    path('login', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('logout', views.userlogout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),

]