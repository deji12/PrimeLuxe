from django.shortcuts import render, get_object_or_404
from .models import Testimonial
from Car.models import Car
from django.conf import settings

def home(request):
    
    cars = Car.objects.all().order_by('created_at') 
    testimonials = Testimonial.objects.all()

    context = {
        'cars': cars,
        'hero_section_images': [car.image.url for car in cars],
        'testimonials': testimonials,
        'car_types': settings.CAR_TYPES
    }

    return render(request, 'home/index2.html', context)