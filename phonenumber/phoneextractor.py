import phonenumbers
from phonenumbers import timezone, geocoder, carrier
  
# Parsing String to Phone number
def get_phone_data(number):
  phoneNumber = phonenumbers.parse(number)
  return {
      "baisc-data": phoneNumber,
      "time-zone": timezone.time_zones_for_number(phoneNumber),
      "career": carrier.name_for_number(phoneNumber, 'en'),
      "is_valid": phonenumbers.is_valid_number(phoneNumber),
      "is_possible": phonenumbers.is_possible_number(phoneNumber)
  }

print(get_phone_data("+91XXXXXXXXXX"))
