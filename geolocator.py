import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

data_file_path = 'datafiles/'
rest_data_file = '{}{}'.format(data_file_path, 'sample_rest_data.json')
new_file_name = 'full_rest_info.json'

geolocator = Nominatim(user_agent='locator')
df = pd.read_json(rest_data_file, lines=True)


def location_to_address(location_dict):
    street = location_dict['address'][0]
    state = location_dict['state']
    code = location_dict['postal_code']
    address = '{}, {}, {}'.format(street, state, code)
    
    return address


def address_to_latlong(address):
    try:
        location = geolocator.geocode(address)
    except GeocoderTimedOut as e:
        print('timeout')
        location = None
    if location is None:
        print(address)
        return None
    else:
        return (location.latitude, location.longitude)

df['address'] = df['location'].apply(location_to_address)
df['lat-long'] = df['address'].apply(address_to_latlong)

df.to_json(data_file_path + new_file_name)
