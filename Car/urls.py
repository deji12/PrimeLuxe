from django.urls import path
from . import views

urlpatterns = [
    path('fleet/<slug:slug>/', views.listing_detail, name='listing'),
    path('fleet/', views.fleet, name='fleet'),
]