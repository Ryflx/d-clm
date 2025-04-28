from django.urls import path
from django.contrib.auth import views as auth_views
from users import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('docusign-settings/', views.docusign_settings, name='docusign_settings'),
    path('docusign-auth/', views.docusign_auth, name='docusign_auth'),
    path('docusign-callback/', views.docusign_callback, name='docusign_callback'),
]
