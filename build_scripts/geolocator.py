from geopy.geocoders import Nominatim, ArcGIS, OpenCage, OpenMapQuest
from geopy.exc import GeocoderTimedOut, GeocoderQuotaExceeded, GeocoderInsufficientPrivileges
import os

nomatim = Nominatim(user_agent='locators')
arcgis = ArcGIS(timeout=10)
geocoders = [nomatim, arcgis]

if 'OPEN_CAGE_API_KEY' in os.environ:
    geocoders.append(OpenCage(os.environ['OPEN_CAGE_API_KEY']))

if 'OPEN_MAP_QUEST_API_KEY' in os.environ:
    geocoders.append(OpenMapQuest(os.environ['OPEN_MAP_QUEST_API_KEY']))


for i in range(len(geocoders)):
    geocoders[i] = geocoders[i].geocode


def address_to_lat_long(df):
    df['lat-long'] = df['address'].apply(convert)


def convert(address):
    i = 0

    if address is None:
        return None

    while i < len(geocoders):
        try:
            location = geocoders[i](address)
            if location is not None:
                return location.latitude, location.longitude
            else:
                i += 1
        except GeocoderTimedOut as timeout:
            i += 1
        except (GeocoderQuotaExceeded, GeocoderInsufficientPrivileges) as quota:
            geocoders.pop(i)
            print("quota exceeded")
        except Exception:
            print("Something else happened", address)
            return None

    print("Not Found: ", address)
    return None

