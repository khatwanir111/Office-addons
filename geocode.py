from geopy.geocoders import Nominatim

def print_data(location):
  print("Address: ",location.address)
  print("Latitude: ", location.latitude)
  print("Longitude: ",location.longitude)

geolocator = Nominatim(user_agent="gfg_app")

def geocoding(address):
  location = geolocator.geocode(address)
  print_data(location)

def rev_geocoding(latitude_longitude):
  location = geolocator.reverse(latitude_longitude)
  print_data(location)

geocoding("175 5th Avenue NYC")
rev_geocoding("52.509669, 13.376294")
