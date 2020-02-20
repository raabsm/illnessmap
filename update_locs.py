import pandas as pd
import sys
import geolocator

file_path = '../datafiles/'
file_name = 'updated_rest_data.json'
df = pd.read_json(file_path + file_name)


def location_to_address(location_dict):
    street = location_dict['address'][0]
    state = location_dict['state']
    code = location_dict['postal_code']
    address = '{}, {}, {}'.format(street, state, code)

    return address

def location_to_lat_long(location_dict):
    latitude = location_dict['coordinate']['latitude']
    longitude = location_dict['coordinate']['longitude']

    if latitude is  None or longitude is None:
        return None
    else:
        return (latitude, longitude)

def address_to_lat_long(address, lat_long):
    if lat_long is not None:
        return lat_long
    else:
        return geolocator.convert(address)


df['address'] = df['location'].apply(location_to_address)
df['lat-long'] = df['location'].apply(location_to_lat_long)
df['if_geopy'] = df['lat-long'].apply(lambda x: False if x is not None else True)
df['lat-long'] = df.apply(lambda x: address_to_lat_long(x['address'], x['lat-long']), axis=1)

df.to_json('written_from_py.json')



