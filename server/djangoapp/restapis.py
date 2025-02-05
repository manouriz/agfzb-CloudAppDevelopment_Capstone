import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

def get_request(url, **kwargs):
    #print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = None
        if "api_key" in kwargs:
            api_key = str(kwargs["api_key"])
            response = requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'})

        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        return json_data
    except Exception as e:
        # If any error occurs
        print("Network exception occurred: " + str(e))
# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["body"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=str(dealer["address"]), city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url+"?dealerId=" + str(dealerId))
    if 'result' in json_result:
        # Get the row list in JSON as dealers
        reviews = json_result["result"]
        # For each dealer object
        for rev in reviews:
            rev_obj = DealerReview(id = int(rev["id"]),dealership = int(rev["dealership"]),name = str(rev["name"]),purchase = bool(rev["purchase"]),review = str(rev["review"]),purchase_date = str(rev["purchase_date"]),car_make = str(rev["car_make"]),car_model = str(rev["car_model"]),car_year = int(rev["car_year"]))
            rev_obj.sentiment = analyze_review_sentiments(rev_obj.review)
            results.append(rev_obj)

    return results


# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_by_id_from_cf(url, dealerId):
    print('> Getting dealer\'s cars by dealer\'s id')
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url+"?dealerId=" + str(dealerId))
    if json_result:
        #print("> json_result: ", json_result)
        # Get the row list in JSON as dealers
        dealers = json_result["body"]["docs"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            # Create a CarDealer object with values in `doc` object
            #print("> Dealer: ", dealer)
            dealer_obj = CarDealer(
                address = dealer["address"], 
                city = dealer["city"], 
                full_name = dealer["full_name"],
                id = dealer["id"], 
                lat = dealer["lat"], 
                long = dealer["long"],
                short_name = dealer["short_name"],
                st = dealer["st"], 
                zip = dealer["zip"])
            results.append(dealer_obj)

    return results

def get_dealer_by_state_from_cf(url, state):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url+"?state=" + state)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["body"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=str(dealer["address"]), city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)

    return results[0]


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealerreview, **kwargs):
    api_key = "hSLjbfo4T-VGpG6W5dXIBw5LALN4RbvhWb1z7ijo5Uy4"
    url = "https://api.eu-de.natural-language-understanding.watson.cloud.ibm.com/instances/dc2f04f6-8c88-4d9d-8cf6-025f68af17fd/v1/analyze?version=2019-07-12"
    params = dict()
    params["text"] = dealerreview
    #params["version"] = kwargs["version"]
    params["features"] = {"sentiment": {}}    
    #params["return_analyzed_text"] = kwargs["return_analyzed_text"]
    response = requests.post(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
    json_response = response.json()
    if "sentiment" in json_response:
        return json_response["sentiment"]["document"]["label"]
    else:
        return json_response


def post_request(url, json_payload, **kwargs):
    try:
        print(json_payload)
        response = requests.post(url, params=kwargs, headers={'Content-Type': 'application/json'}, data=json_payload)
        status_code = response.status_code
        print("> Response Status {} ".format(status_code))
        #json_data = json.loads(response.text)
        return response.text
    except Exception as e:
        print("Network exception occurred: " + str(e))
        return {"error",str(e)}


