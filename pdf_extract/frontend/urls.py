
from django.urls import path
from .views import index

urlpatterns = [
    path('', index),
    path('student/<str:studentCode>', index)
]
