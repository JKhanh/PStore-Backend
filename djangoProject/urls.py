"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from pstore import views as store_view
from authenticate import views as auth_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/products', store_view.ListCreateProductView.as_view()),
    path('api/v1/products/<int:pk>/reviews', store_view.ListReviewByProduct.as_view()),
    # url(regex=r'^api/v1/products(?\w{1,100})', view=store_view.ListCreateProductView.as_view()),
    path('api/v1/register', view=auth_view.UserRegisterView.as_view()),
    path('api/v1/login', jwt_views.TokenObtainPairView.as_view()),
]
