import geoip2.database

def get_country(ip):
        reader = geoip2.database.Reader('./geoip/GeoLite2-City.mmdb')
        response = reader.city(ip)
        return response.country.name
        
