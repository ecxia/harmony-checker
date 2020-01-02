"""harmony URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from harmony_checker.views import profile
from harmony_checker.forms import AuthFormWithSubmit, PasswordChangeFormWithSubmit, PwdResetFormWithSubmit
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'harmony_checker/', 
        include('harmony_checker.urls', namespace='harmony_checker'),
    ),
    path('accounts/login/', LoginView.as_view(authentication_form = AuthFormWithSubmit), name='login'),
    path('accounts/password_change/', PasswordChangeView.as_view(form_class = PasswordChangeFormWithSubmit), name='pwd_change'),
    path('accounts/password_reset/', PasswordResetView.as_view(form_class = PwdResetFormWithSubmit), name='pwd_reset'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/', include('django.contrib.auth.urls')),
]
