from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.text import slugify
from django.urls import reverse

CAR_TYPES = [
    ('sedan', 'Sedan'),
    ('suv', 'SUV'),
    ('hatchback', 'Hatchback'),
    ('convertible', 'Convertible'),
    ('coupe', 'Coupe'),
    ('wagon', 'Wagon'),
    ('pickup', 'Pickup Truck'),
]

FUEL_TYPES = [
    ('gasoline', 'Gasoline'),
    ('electric', 'Electric'),
    ('hybrid', 'Hybrid'),
]

TRANSMISSION_TYPES = [
    ('automatic', 'Automatic'),
    ('manual', 'Manual'),
    ('cvt', 'CVT'),
    ('semi-automatic', 'Semi-Automatic'),
    ('dual-clutch', 'Dual-Clutch (e.g., LDF, F1)'),
    ('tiptronic', 'Tiptronic'),
]

LUXURY_CAR_BRANDS = [
    ('Acura', 'Acura'),
    ('Alfa Romeo', 'Alfa Romeo'),
    ('Aston Martin', 'Aston Martin'),
    ('Audi', 'Audi'),
    ('Bentley', 'Bentley'),
    ('BMW', 'BMW'),
    ('Bugatti', 'Bugatti'),
    ('Cadillac', 'Cadillac'),
    ('Ferrari', 'Ferrari'),
    ('Genesis', 'Genesis'),
    ('Infiniti', 'Infiniti'),
    ('Jaguar', 'Jaguar'),
    ('Koenigsegg', 'Koenigsegg'),
    ('Lamborghini', 'Lamborghini'),
    ('Land Rover', 'Land Rover'),
    ('Lexus', 'Lexus'),
    ('Lincoln', 'Lincoln'),
    ('Lotus', 'Lotus'),
    ('Lucid', 'Lucid'),
    ('Maserati', 'Maserati'),
    ('Maybach', 'Maybach'),
    ('McLaren', 'McLaren'),
    ('Mercedes-Benz', 'Mercedes-Benz'),
    ('Pagani', 'Pagani'),
    ('Porsche', 'Porsche'),
    ('Rolls-Royce', 'Rolls-Royce'),
    ('Range Rover', 'Range Rover'),
    ('Tesla', 'Tesla'),
]


class CarAmenity(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="The name of the car amenity (e.g., Bluetooth, Sunroof, Navigation).")
    icon = models.CharField(max_length=100, blank=True, null=True, help_text="Optional icon class or reference used to visually represent the amenity.")
    is_search_filter_enabled = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Car Amenity'
        verbose_name_plural = 'Car Amenities'


class Car(models.Model):
    name = models.CharField(max_length=100, help_text="The display name of the car (e.g., Mercedes G-Wagon).")
    brand = models.CharField(max_length=50, choices=LUXURY_CAR_BRANDS, help_text="The brand or manufacturer of the car (e.g., Mercedes, BMW).")
    list_description = models.TextField(null=True, blank=True, help_text="A short summary of the car shown in list views.")
    detailed_description = CKEditor5Field('Text', config_name='extends', null=True, blank=True, help_text="A detailed and formatted description shown on the car detail page.")
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True, help_text="URL-friendly identifier for the car, auto-generated from the name.")
    image = models.ImageField(upload_to='cars/', null=True, blank=True, help_text="Main image of the car used in listings.")
    body_type = models.CharField(max_length=20, choices=CAR_TYPES, default='sedan', help_text="The body style of the car, such as SUV, Sedan, Coupe, etc.")
    seats = models.PositiveIntegerField(default=4, help_text="The number of passenger seats in the car.")
    doors = models.PositiveIntegerField(default=4, help_text="The number of doors available on the car.")
    amenities = models.ManyToManyField(CarAmenity, related_name='cars', help_text="Select all available amenities for this car.")
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2, help_text="Daily rental price for the car.")
    is_available = models.BooleanField(default=True, help_text="Toggle whether the car is currently available for booking.")
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPES, default='petrol', help_text="Type of fuel the car uses (Petrol, Diesel, Electric, etc.).")
    horsepower = models.CharField(max_length=50, help_text="The car’s engine power measured in horsepower.")
    transmission = models.CharField(max_length=50, default='automatic', help_text="Type of transmission system (e.g., Automatic, Manual).")
    rating = models.FloatField(default=0, help_text="Average user rating for the car, typically from 1 to 5 stars.")
    video_link = models.URLField(max_length=200, null=True, blank=True, help_text="Optional video URL showcasing the car.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the car entry was created.")

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            count = 1
            while Car.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{count}"
                count += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def car_images(self):
        return CarImage.objects.filter(car=self)
    
    def number_of_images(self):
        return self.car_images().count()

    def get_absolute_url(self):

        return reverse('listing', kwargs={'slug': self.slug})


class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images', help_text="The car this image is associated with.")
    image = models.ImageField(upload_to='car_images/', help_text="An additional image for this car.")

    def __str__(self):
        return f"{self.car.name} - Image {self.id}"


class Review(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='reviews', help_text="The car that this review is about.")
    name = models.CharField(max_length=100, help_text="Name of the person leaving the review.")
    email = models.EmailField(help_text="Email address of the reviewer.")
    message = models.TextField(help_text="Content of the review message.")
    rating = models.PositiveSmallIntegerField(default=0, help_text="Rating given by the user (1 to 5 stars).")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time the review was submitted.")

    def __str__(self):
        return f"{self.name} - {self.rating} stars"
