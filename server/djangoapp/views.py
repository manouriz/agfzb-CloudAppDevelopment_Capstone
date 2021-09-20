from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_request, get_dealers_from_cf, get_dealer_reviews_from_cf, get_dealer_by_id_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def template_01(request):
    context = {}
    return render(request, 'djangoapp/template-01.html', context)

# Create an `about` view to render a static about page
def about_request(request):
    context = {}
    return render(request, 'djangoapp/about.html', context)

# Create a `contact` view to return a static contact page
def contact_request(request):
    context = {}
    return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    return render(request, 'djangoapp/registration.html', context)



# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://176f6788.eu-de.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context = {'dealerships':dealerships}
        # Concat all dealer's short name
        # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        # return HttpResponse(dealer_names)
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    context = {'dealer_id':dealer_id, 'dealer_name':'test'}
    if request.method == "GET":
        url = "https://176f6788.eu-de.apigw.appdomain.cloud/api/review"
        # Get dealers from the URL
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        context['reviews'] = reviews
        # Concat all dealer's short name
        # rev_names = ' '.join([rev.name for rev in reviews])
        # result = ''
        # for rev in reviews:            
        #    result += rev.name + ": " + str(rev.sentiment) + "<br>"
        # Return a list of dealer short name
        # return HttpResponse(result)
        return render(request, 'djangoapp/dealer_details.html', context)



# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):
    context = {'dealer_id':dealer_id}
    user = request.user
    if user.is_authenticated:        
        if request.method == 'GET':
            url = "https://176f6788.eu-de.apigw.appdomain.cloud/api/dealership"
            cars = get_dealer_by_id_from_cf(url,dealer_id)
            context['cars'] = cars
            return render(request, 'djangoapp/add_review.html', context)

        elif request.method == 'POST':
            url = "https://176f6788.eu-de.apigw.appdomain.cloud/api/review"        
            payload = json.dumps({
            "review": {
                "id": 1116,
                "name": "Alphread Hichkak",
                "dealership": 15,
                "review": "This was not a great car dealer!",
                "purchase": False,
                "another": "field",
                "purchase_date": "02/16/2021",
                "car_make": "Audi",
                "car_model": "Car",
                "car_year": 2021                             
            }
            })        
            result = post_request(url,payload)
            redirect("djangoapp:dealer_details", dealer_id=dealer_id)
    else:
        return HttpResponse({"error", "User not logged in!"})


