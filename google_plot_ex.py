import re
import pandas as pd
import folium

def extract_city_info(news_text, country_names):
    city_info = []
    # Regular expression pattern to find ", country_name" occurrences
    pattern = r'(.+?),\s*(' + '|'.join(country_names) + r')\b'
    # Find all matches in the text
    matches = re.finditer(pattern, news_text)
    for match in matches:
        # Extract the city name and country name
        city = match.group(1)
        country = match.group(2)
        # Search for coordinates and range after the city mention
        coordinates_match = re.search(r'Coordinates:\s*(\d+\.\d+[NS])\s+(\d+\.\d+[EW])', news_text[match.end():])
        if coordinates_match:
            coordinates = coordinates_match.group(1) + ' ' + coordinates_match.group(2)
            # Search for range after the city mention
            range_match = re.search(r'Range:\s*(\d+)\s*kilometers', news_text[match.end():])
            if range_match:
                range_str = range_match.group(1) + " kilometers"
            else:
                range_str = "Not specified"
            # Append city info to the list
            city_info.append((city.strip(), country.strip(), coordinates, range_str))
    return city_info

# Read the news text file with UTF-8 encoding
with open('C:/Users/niruy/Desktop/weatherradarsites.txt', 'r', encoding='utf-8') as file:
    news_text = file.read()

# List of country names
country_names = ['Albania', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Bermuda', 'Botswana', 'Brazil', 'Brunei', 'Bulgaria', 'Cambodia', 'Canada', 'Cayman Islands', 'China', 'Colombia', 'Costa Rica', 'Croatia', 'Cuba', 'Curacao', 'Cyprus', 'Czechia', 'Denmark', 'Dominican Republic', 'Ecuador', 'El Salvador', 'Estonia', 'Fiji', 'Finland', 'France', 'French Guiana', 'Georgia', 'Germany', 'Greece', 'Guadeloupe', 'Guam', 'Guatemala', 'Guyana', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kuwait', 'Laos', 'Latvia', 'Lebanon', 'Lithuania', 'Macau', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique', 'Mauritius', 'Mexico', 'Moldova', 'Mongolia', 'Morocco', 'Mozambique', 'Myanmar', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Nigeria', 'Norfolk Island', 'North Macedonia', 'Norway', 'Oman', 'Pakistan', 'Panama', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Reunion', 'Romania', 'Russia', 'Rwanda', 'Saudi Arabia', 'Serbia', 'Singapore', 'Sint Maarten', 'Slovakia', 'Slovenia', 'South Africa', 'South Korea', 'Spain', 'Sri Lanka', 'Suriname', 'Sweden', 'Switzerland', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uzbekistan', 'Venezuela', 'Vietnam', 'Zimbabwe']

# Extract city info mentioned in the news text
city_info = extract_city_info(news_text, country_names)

# Create a DataFrame
df = pd.DataFrame(city_info, columns=["City", "Country", "Coordinates", "Range"])

# Print the DataFrame
#print(df)



# Calculate the mean latitude and longitude for centering the map
center_lat = df['Coordinates'].str.extract(r'(\d+\.\d+)[NS]').astype(float).mean()
center_lng = df['Coordinates'].str.extract(r'(\d+\.\d+)[EW]').astype(float).mean()

print("Center Latitude:", center_lat)
print("Center Longitude:", center_lng)

# Initialize the map
mymap = folium.Map(location=[center_lat, center_lng], zoom_start=5)

# Extract latitudes, longitudes, cities, countries, and ranges from the DataFrame
lats = df['Coordinates'].str.extract(r'(\d+\.\d+)[NS]').astype(float)
lngs = df['Coordinates'].str.extract(r'(\d+\.\d+)[EW]').astype(float)
cities = df['City']
countries = df['Country']
ranges = df['Range']

# Add markers for each coordinate with city, country, and range labels
#for lat, lng, city, country, range_val in zip(lats, lngs, cities, countries, ranges):
for x in range (0, len(lats)-1):
    print("Latitude:", lats[x], "Longitude:", lngs[x])
    '''
    # Create HTML content for the marker popup
    popup_text = f"<b>City:</b> {cities[x]} <br> <b>Country:</b> {countries[x]} <br> <b>Range:</b> {ranges[x]}"
    # Add marker to the map
    folium.Marker(
        location=[lats[x], lngs[x]],
        popup=folium.Popup(popup_text, parse_html=True),
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(mymap)

# Save the map to an HTML file
mymap.save("map_with_labels_and_range_folium.html")
'''


'''
# Set the center of the map (you might need to adjust this based on your data)
center_lat = df['Coordinates'].str.extract(r'(\d+\.\d+)[NS]').astype(float).mean()
center_lng = df['Coordinates'].str.extract(r'(\d+\.\d+)[EW]').astype(float).mean()

# Initialize the map
gmap = gmplot.GoogleMapPlotter(center_lat, center_lng, 5)

# Extract latitudes, longitudes, cities, countries, and ranges from the DataFrame
lats = df['Coordinates'].str.extract(r'(\d+\.\d+)[NS]').astype(float)
lngs = df['Coordinates'].str.extract(r'(\d+\.\d+)[EW]').astype(float)
cities = df['City']
countries = df['Country']
ranges = df['Range']

# Add markers for each coordinate with city, country, and range labels
for lat, lng, city, country, range_val in zip(lats, lngs, cities, countries, ranges):
    gmap.marker(lat, lng, title=f"{city}, {country}", label=range_val)

# Save the map to an HTML file
gmap.draw("map_with_labels_and_range.html")
'''