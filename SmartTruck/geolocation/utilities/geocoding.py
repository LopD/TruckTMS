import requests

class Geocoder:
    """
    For decoding geo coordinates to a human readable text.
    """
    def __init__(self, provider="osm", api_key=None, user_agent="smarttuck-KMS-express"):
        self.provider = provider.lower()
        self.api_key = api_key
        self.user_agent = user_agent

    def geocode(self, address: str):
        """Convert address to (lat, lng, display_name, address_in_city, city, state)"""
        if self.provider == "google":
            raise ValueError("Google geocoding has not been tested yet")
            return self._geocode_google(address)
        elif self.provider == "osm":
            return self._geocode_osm(address)
        else:
            raise ValueError("Unsupported provider")

    def reverse_geocode(self, lat: float, lon:float):
        """Convert (lat, lng) to (lat, lng, display_name, address_in_city, city, state)"""
        if self.provider == "google":
            raise ValueError("Google geocoding has not been tested yet")
            return self._reverse_google(lat, lon)
        elif self.provider == "osm":
            return self._reverse_osm(lat, lon)
        else:
            raise ValueError("Unsupported provider")

    ## Google API has not been tested
    def _geocode_google(self, address):
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "address": address,
            "key": self.api_key
        }
        response = requests.get(url, params=params)
        data = response.json()
        if data['status'] != 'OK':
            raise Exception("Google Geocoding Error: " + data['status'])
        location = data['results'][0]['geometry']['location']
        return location['lat'], location['lng']

    ## Google API has not been tested
    def _reverse_google(self, lat, lon):
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "latlng": f"{lat},{lon}",
            "key": self.api_key
        }
        response = requests.get(url, params=params)
        data = response.json()
        if data['status'] != 'OK':
            raise Exception("Google Reverse Geocoding Error: " + data['status'])
        return data['results'][0]['formatted_address']

    def _geocode_osm(self, address: str):
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": address,
            "format": "json",
            "addressdetails": 1, ## get detailed representation
            "limit": 1           ## get only one result of the X results returned
        }
        headers = {"User-Agent": self.user_agent}
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        if not data:
            raise Exception("OSM Geocoding Error: No results found")
        
        address_data = data.get("address", {})
        address_in_city =  ",".join([address_data.get("house_number"),address_data.get("road"),address_data.get("suburb")])
        city = address_data.get("city") or address_data.get("town") or address_data.get("village") or address_data.get("hamlet")
        state = address_data.get("state")

        return float(data['lat']), float(data['lon']), data['display_name'], address_in_city, city, state

    def _reverse_osm(self, lat:float, lon:float):
        url = "https://nominatim.openstreetmap.org/reverse"
        params = {
            "lat": lat,
            "lon": lon,
            "format": "json",
            "addressdetails": 1, ## get detailed representation
            "limit": 1,          ## get only one result of the X results returned
        }
        headers = {"User-Agent": self.user_agent}
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        if 'error' in data:
            raise Exception("OSM Reverse Geocoding Error: " + data['error'])
        
        address_data = data.get("address", {})
        address_in_city =  ",".join([address_data.get("house_number",""),address_data.get("road",""),address_data.get("suburb","")])
        city = address_data.get("city") or address_data.get("town") or address_data.get("village") or address_data.get("hamlet") or address_data.get("municipality") or address_data.get("county") or "unknown"
        state = address_data.get("state")

        return float(data['lat']), float(data['lon']), data['display_name'], address_in_city, city, state

    ## NOT USED:
    def get_city_and_state(address: str):
        """Returns the city name and 2-letter US state abbreviation from an address using Nominatim."""
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": address,
            "format": "json",
            "addressdetails": 1,
            "limit": 1
        }
        headers = {
            "User-Agent": "YourAppName/1.0 (your.email@example.com)"
        }

        response = requests.get(url, params=params, headers=headers)
        if response.status_code != 200:
            raise Exception("API request failed")

        data = response.json()
        if not data:
            return None, None

        address_data = data[0].get("address", {})
        city = address_data.get("city") or address_data.get("town") or address_data.get("village") or address_data.get("hamlet")
        state = address_data.get("state")

        # Optional: convert full state name to 2-letter abbreviation
        us_states = {
            "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
            "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
            "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID",
            "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
            "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
            "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
            "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
            "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY",
            "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
            "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
            "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
            "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV",
            "Wisconsin": "WI", "Wyoming": "WY", "District of Columbia": "DC"
        }
        state_abbr = us_states.get(state)

        return city, state_abbr
