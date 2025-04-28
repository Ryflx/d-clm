from django.urls import path
from settings import views

app_name = 'settings'

urlpatterns = [
    path('', views.app_settings, name='app_settings'),
]
