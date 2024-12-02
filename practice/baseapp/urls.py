"""
URL configuration for practice project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

app_name = "baseapp"

urlpatterns = [
    path('', views.langpage, name="landpage"),
    path('login/', views.login, name="login"),
    path('gmail_login/', views.gmail_login, name="gmail_login"),
    path('gmail_ca/', views.gmail_ca, name="gmail_ca"),
    path('facebook_login/', views.facebook_login, name="facebook_login"),
    path('facebook_ca/', views.facebook_ca, name="facebook_ca"),
    path('create_account/', views.create_account, name="create_account"),
    path('logout/', views.logout, name="logout"),
    path('homepage/', views.homepage, name="homepage"),
    path('profile/', views.profile, name="profile"),
]
