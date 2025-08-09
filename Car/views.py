from django.shortcuts import render, get_object_or_404
from .models import Car, CarAmenity
from django.urls import reverse
from django.db.models import Count
from django.conf import settings

# Create your views here.
def listing_detail(request, slug):

    car = get_object_or_404(Car, slug=slug)
    similar_cars = Car.objects.all().exclude(id=car.id).order_by('-created_at') 

    context = {
        'car': car,
        'similar_cars': similar_cars
    }
    return render(request, 'car/listing-single.html', context)

def fleet(request):

    amenities = CarAmenity.objects.filter(is_search_filter_enabled=True)
    car_types = settings.CAR_TYPES

    if request.method == 'POST':
        print(request.POST)
        fuel_type = request.POST.get('fuel')
        car_type = request.POST.get('car_type')
        seat = request.POST.get('seats')
        doors = request.POST.get('doors')
        selected_amenities = request.POST.getlist('amenities')
        sort_by = request.POST.get('sort_by')

        cars = Car.objects.all()

        for car in cars:
            print(car.fuel_type)
            print(car.body_type)
        
        if fuel_type:
            cars = cars.filter(fuel_type=fuel_type)

        if car_type and car_type != 'All types':
            cars = cars.filter(body_type=car_type)

        if seat:
            cars = cars.filter(seats=int(seat))

        if doors:
            cars = cars.filter(doors=int(doors))
        
        if selected_amenities:
            cars = (
                Car.objects
                .filter(amenities__name__in=selected_amenities)
                .annotate(num_matches=Count('amenities', distinct=True))
                .filter(num_matches=len(selected_amenities))
            )

        if sort_by:
            if sort_by == 'latest':
                cars.order_by('-id')
            elif sort_by == 'ascending_price':
                cars = cars.order_by('price_per_day')
                print(f'ascending ordered_cars: {cars}')
            elif sort_by == 'decending_price':
                cars = cars.order_by('-price_per_day')
                print(f'decending ordered_cars: {cars}')


        cars = cars.distinct()

        context = {
            'cars': cars,
            'num_cars': cars.count(),
            'amenities': amenities,
            'fuel_type': fuel_type,
            'car_type': car_type,
            'seats': seat,
            'doors': doors,
            'selected_amenities': selected_amenities,
            'car_types': car_types,
            'sort_by': sort_by
        }
        return render(request, 'car/fleet.html', context)
            
    cars = Car.objects.all()

    context = {
        'cars': cars,
        'num_cars': cars.count(),
        'amenities': amenities,
        'car_types': car_types
    }

    return render(request, 'car/fleet.html', context)