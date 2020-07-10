import sys
import geolocator
from mongodb_connection import MongoConnection
import api_keys


def location_to_address(location_dict):
    street = location_dict['address'][0]
    state = location_dict['state']
    code = location_dict['postal_code']
    address = '{}, {}, {}'.format(street, state, code)

    return address


def location_to_lat_long(location_dict):
    latitude = location_dict['coordinate']['latitude']
    longitude = location_dict['coordinate']['longitude']

    if latitude is None or longitude is None:
        return None
    else:
        return latitude, longitude


def address_to_lat_long(address):
    return geolocator.convert(address)


def create_fields_from_location(location_dict):
    to_return = {}
    to_return['address'] = location_to_address(location_dict)
    coordinates_given = location_to_lat_long(location_dict)
    to_return['lat-long'] = coordinates_given if coordinates_given is not None \
        else address_to_lat_long(to_return['address'])
    to_return['if_geopy'] = False if coordinates_given else True

    return to_return


if __name__ == '__main__':

    if len(sys.argv) != 3:
        print("Usage: update_locs <DB> <Collection>")
        sys.exit()
    else:
        db, col = sys.argv[1], sys.argv[2]

    try:
        db = MongoConnection(db, api_keys.DB_INFO['uri'])
        collection = db.return_collection(col)
    except Exception as e:
        print('Error while connecting: ', e)
        sys.exit()

    docs_without_lat_long = collection.find({'lat-long': None}, no_cursor_timeout=True)
    for doc in docs_without_lat_long:
        location_dict = doc['location']
        to_insert = create_fields_from_location(location_dict)
        collection.update_one({'_id': doc['_id']}, {'$set': to_insert})

    docs_without_lat_long.close()
