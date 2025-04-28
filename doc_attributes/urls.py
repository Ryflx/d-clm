from django.urls import path
from doc_attributes import views

app_name = 'doc_attributes'

urlpatterns = [
    path('', views.document_attributes, name='document_attributes'),
]
