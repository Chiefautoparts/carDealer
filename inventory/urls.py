from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
	path('', views.home, name='home'),
	path('inventory/', views.inventory, name='inventory'),
	path('car/<int:pk>/', views.car_detail, name='car_detail'),
	path('contact/', views.contact, name='contact'),
]