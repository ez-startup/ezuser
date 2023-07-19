import geoip2.database
from iam.settings import GEOIP_PATH

database_name = "GeoIP2-City.mmdb"
def get_geoip_data(ip_address, database_name):
    try:
        reader = geoip2.database.Reader(GEOIP_PATH + database_name)
        response = reader.city(ip_address)
        # Perform necessary operations with the response
        reader.close()
        return response
    except:
        return None
