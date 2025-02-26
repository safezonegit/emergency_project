from django.urls import path
from . import views

urlpatterns = [
    path('',views.homepage,name='home'),
    path('about/',views.contact,name='contact'),
    path('responders/',views.responders,name='responders'),
    path('report/', views.anonymous_response_create, name='anonymous_response_create'),
]