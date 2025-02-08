from django.urls import path
from . import views


urlpatterns = [
    path('', views.save_incident,name='save_incident'),
    path('success/',views.incident_report_success,name='success'),   
]