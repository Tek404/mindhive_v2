import requests
from django.conf import settings

def get_geocode(address):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        'address': address,
        'key': settings.GOOGLE_MAPS_API_KEY,
    }
    print("Geocoding API Request URL:", requests.Request('GET', base_url, params=params).prepare().url)
    response = requests.get(base_url, params=params)
    data = response.json()
    print("Geocoding API Response:", data)

    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    else:
        return None