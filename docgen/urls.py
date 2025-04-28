from django.urls import path
from docgen import views

app_name = 'docgen'

urlpatterns = [
    path('form/', views.docgen_form, name='docgen_form'),
]
