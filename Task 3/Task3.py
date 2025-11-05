
# Import required libraries
import requests      # For HTTP requests
import csv           # For writing CSV files


# Get city coordinates (latitude, longitude) using Nominatim geocoding API
def get_city_coordinates(city_name):
    """Get city coordinates using Nominatim geocoding service."""
    nominatim_url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': city_name,
        'format': 'json',
        'limit': 1,
        'countrycodes': 'IN' 
    }

    headers = {'User-Agent': 'TouristAttractionsScraper/1.0'}

    try:
        response = requests.get(nominatim_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data:
            # Return latitude and longitude as floats
            return float(data[0]['lat']), float(data[0]['lon'])
        else:
            print(f"Could not find coordinates for: {city_name}")
            return None, None
    except Exception as e:
        print(f"Error getting coordinates: {e}")
        return None, None


# Fetch tourist attractions for a city using Overpass API and OpenStreetMap
def fetch_tourist_attractions(city_name):
    overpass_url = "http://overpass-api.de/api/interpreter"

    # Get city coordinates using Nominatim
    city_lat, city_lon = get_city_coordinates(city_name)

    if city_lat is None or city_lon is None:
        return []

    print(f"Found {city_name} at coordinates: {city_lat}, {city_lon}")

    # Overpass QL query to find various types of attractions within 50km
    query = f"""
    [out:json];
    (
      node["tourism"~"museum|attraction|zoo|theme_park|viewpoint|artwork"](around:50000,{city_lat},{city_lon});
      way["tourism"~"museum|attraction|zoo|theme_park|viewpoint|artwork"](around:50000,{city_lat},{city_lon});
      node["historic"~"monument|memorial|castle|ruins|archaeological_site"](around:50000,{city_lat},{city_lon});
      way["historic"~"monument|memorial|castle|ruins|archaeological_site"](around:50000,{city_lat},{city_lon});
      node["leisure"="park"](around:50000,{city_lat},{city_lon});
      way["leisure"="park"](around:50000,{city_lat},{city_lon});
      node["amenity"~"place_of_worship|theatre|cinema"](around:50000,{city_lat},{city_lon});
      way["amenity"~"place_of_worship|theatre|cinema"](around:50000,{city_lat},{city_lon});
    );
    out center;
    """

    try:
        # Send POST request to Overpass API
        response = requests.post(overpass_url, data={'data': query}, timeout=30)
        response.raise_for_status()
        data = response.json()

        attractions = []
        for element in data['elements']:
            tags = element.get('tags', {})
            name = tags.get('name', 'Unknown')
            # Determine type of attraction
            tourism_type = (tags.get('tourism') or tags.get('historic') or
                          tags.get('leisure') or tags.get('amenity') or 'Unknown')
            # Get coordinates
            lat = element.get('lat') or element.get('center', {}).get('lat')
            lon = element.get('lon') or element.get('center', {}).get('lon')

            # Only add if name and coordinates are present
            if lat and lon and name != 'Unknown':
                attractions.append({
                    'name': name,
                    'type': tourism_type,
                    'latitude': lat,
                    'longitude': lon
                })

        return attractions

    except requests.exceptions.RequestException as e:
        print(f"Error fetching attractions data: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []


# Save the list of attractions to a CSV file
def save_to_csv(data, city_name):
    if not data:
        print(f"No attractions found for {city_name}")
        return

    filename = f"tourist_attractions_{city_name.replace(' ', '_')}.csv"
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'type', 'latitude', 'longitude']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print(f"✓ Saved {len(data)} attractions to {filename}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")


# Main execution block
if __name__ == "__main__":
    city = "Surat"
    print(f"Fetching tourist attractions for {city}...")
    attractions = fetch_tourist_attractions(city)

    if attractions:
        print(f"Found {len(attractions)} attractions")
        save_to_csv(attractions, city)
    else:
        print(f"No attractions found for {city}. Try a different city or check the city name.")
