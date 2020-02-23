import pandas as pd
import sys
import geolocator

if len(sys.argv) != 2:
    print("Usage: update_locs <path_to_file>")
    sys.exit()

path_to_file = sys.argv[1]

try:
    df = pd.read_json(path_to_file)
except ValueError as e:
    df = pd.read_json(path_to_file, lines=True)


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

if 'address' not in df.columns:
    df['address'] = df['location'].apply(location_to_address)

if 'lat-long' not in df.columns:
    df['lat-long'] = df['location'].apply(location_to_lat_long)
    df['if_geopy'] = df['lat-long'].apply(lambda x: False if x is not None else True)
df['lat-long'] = df.apply(lambda x: address_to_lat_long(x['address'], x['lat-long']), axis=1)

df.to_json(path_to_file)



