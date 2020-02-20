import pandas as pd
from geopy.geocoders import Nominatim, ArcGIS, OpenCage, OpenMapQuest
from geopy.exc import GeocoderTimedOut, GeocoderQuotaExceeded, GeocoderInsufficientPrivileges
from geopy.extra.rate_limiter import RateLimiter
import api_keys

nomatim = Nominatim(user_agent='locators')
arcgis = ArcGIS(timeout=10)
opencage = OpenCage(api_keys.OpenCage_API_KEY)
openmapquest = OpenMapQuest(api_keys.OpenMapQuest_API_KEY)

geocoders = [nomatim, arcgis, opencage, openmapquest]

for i in range(len(geocoders)):
    #rate_limiter = RateLimiter(geocoders[i].geocode, min_delay_seconds=1)
    #geocoders[i] = rate_limiter
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
            print("Something else happened", address)
            return None

    print("Not Found: ", address)
    return None

