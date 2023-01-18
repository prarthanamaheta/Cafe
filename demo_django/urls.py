from django.contrib import admin
from django.urls import path

from demo_django.views import DashboardMenulistView, CreateFoodView, SignUpView

urlpatterns = [
    path('signup/',SignUpView.as_view(),name='signup'),
    path('menu/', DashboardMenulistView.as_view(), name='menu'),
    path('create-food/', CreateFoodView.as_view(), name='create_food')
]
