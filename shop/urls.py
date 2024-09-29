from django.urls import path
from . import views
urlpatterns = [

    path('', views.home),
    path('discover/', views.discover),
    path('cart/', views.cart),
]