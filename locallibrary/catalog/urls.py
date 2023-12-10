from django.urls import path
from . import views




urlpatterns = [
    path('', views.index, name='index'),  # '' = url pattern , called view "index" in views.py, name = identifier unique (to use in reverse mapping)
]