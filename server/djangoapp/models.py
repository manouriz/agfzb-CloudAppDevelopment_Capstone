from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
# CarMake model
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30, default='Mercedes Benz')
    description = models.CharField(max_length=1000)
    country = models.CharField(max_length=1000)

    def __str__(self):
        return "Name: " + self.name + "," + \
               "Description: " + self.description + "," + \
               "Country: " + self.country


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
# CarModel model
class CarModel(models.Model):
    name = models.CharField(null=False, max_length=30, default='Citroen C5')    
    description = models.CharField(max_length=1000)
    dealerId = models.IntegerField(default=0)
    year = models.IntegerField(default=1990)
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'WAGON'
    OTHERS = 'Others'
    CARTYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'WAGON'),
        (OTHERS, 'Others')
    ]
    carType = models.CharField(
        null=False,
        max_length=20,
        choices=CARTYPE_CHOICES,
        default=OTHERS
    )
    carMake = models.ForeignKey(CarMake, on_delete=models.CASCADE)

    def __str__(self):
        return "Name: " + self.name + "," + \
               "Description: " + self.description + "," + \
               "Dealer ID: " + str(self.dealerId) + "," + \
               "Year: " + str(self.year) + "," + \
               "Car Type: " + str(self.carType) + "," + \
               "Car Make: " + str(self.carMake)

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name


# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview(models.Model):
    id = models.AutoField(primary_key=True)
    #dealership = models.ForeignKey(CarDealer, on_delete=models.CASCADE)
    dealership = models.IntegerField(default=0)
    name = models.CharField(max_length=1000)
    purchase = models.BooleanField()
    review = models.CharField(max_length=1000)
    purchase_date = models.CharField(max_length=1000)
    car_make = models.CharField(max_length=1000)
    car_model = models.CharField(max_length=1000)
    car_year = models.IntegerField(default=1990)
    
    POSITIVE = 'positive'
    NEUTRAL = 'neutral'
    NEGATIVE = 'negative'    
    SENTIMENT_CHOICES = [
        (POSITIVE, 'positive'),
        (NEUTRAL, 'neutral'),
        (NEGATIVE, 'negative')
    ]
    sentiment = models.CharField(
        null=False,
        max_length=20,
        choices=SENTIMENT_CHOICES,
        default=NEUTRAL
    )

