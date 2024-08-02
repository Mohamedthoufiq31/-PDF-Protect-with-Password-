
from django.contrib import admin
from django.urls import path
from protect import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('protected_pdf/', views.protected_pdf, name='protected_pdf'),
]
