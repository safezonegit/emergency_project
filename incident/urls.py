from django.urls import path
from . import views


urlpatterns = [
    path('', views.save_incident,name='save_incident')
]