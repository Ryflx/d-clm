from django.urls import path
from sourcing import views

app_name = 'sourcing'

urlpatterns = [
    path('', views.sourcing_login, name='sourcing_login'),
]
