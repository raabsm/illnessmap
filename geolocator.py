import pandas as pd
from geopy.geocoders import Nominatim, ArcGIS, OpenCage, OpenMapQuest
from geopy.exc import GeocoderTimedOut, GeocoderQuotaExceeded, GeocoderInsufficientPrivileges
from geopy.extra.rate_limiter import RateLimiter
import api_keys

data_file_path = 'datafiles/'
rest_data_file = '{}{}'.format(data_file_path, 'nyc_restaurant_data_geo2.json')
new_file_name = 'geo2_full_rest_info.json'

nomatim = Nominatim(user_agent='locators')
arcgis = ArcGIS(timeout=10)
opencage = OpenCage(api_keys.OpenCage_API_KEY)
openmapquest = OpenMapQuest(api_keys.OpenMapQuest_API_KEY)

geocoders = [nomatim, arcgis, opencage, openmapquest]

for i in range(len(geocoders)):
    #rate_limiter = RateLimiter(geocoders[i].geocode, min_delay_seconds=1) 
    #geocoders[i] = rate_limiter
    geocoders[i] = geocoders[i].geocode


df = pd.read_json(rest_data_file, lines=True)


def location_to_address(location_dict):
    street = location_dict['address'][0]
    state = location_dict['state']
    code = location_dict['postal_code']
    address = '{}, {}, {}'.format(street, state, code)
    
    return address


def address_to_latlong(address):
    i = 0
    
    while i < len(geocoders):
        try:
            location = geocoders[i](address)
            if location != None:
                return (location.latitude, location.longitude)
            else:
                i += 1
        except GeocoderTimedOut as timeout:
            i += 1
        except (GeocoderQuotaExceeded, GeocoderInsufficientPrivileges) as quota:
            geocoders.pop(i)
            print("quota exceeded")
        except Exception:
            print("Something else happened")

    print("Not Found: ", address)
    return None

df['address'] = df['location'].apply(location_to_address)
df['lat-long'] = df['address'].apply(address_to_latlong)

df.to_json(data_file_path + new_file_name)
