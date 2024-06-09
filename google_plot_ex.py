#%%
%clear
%reset -f
import re
import pandas as pd
import matplotlib.pyplot as plt
import folium
plt.close("all")

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
country_names = ['Albania', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Bermuda', 'Botswana', 'Brazil', 'Brunei', 'Bulgaria', 'Cambodia', 'Canada', 'Cayman Islands', 'China', 'Colombia', 'Costa Rica', 'Croatia', 'Cuba', 'Curacao', 'Cyprus', 'Czechia', 'Denmark', 'Dominican Republic', 'Ecuador', 'El Salvador', 'Estonia', 'Fiji', 'Finland', 'France', 'French Guiana', 'Georgia', 'Germany', 'Greece', 'Guadeloupe', 'Guam', 'Guatemala', 'Guyana', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kuwait', 'Laos', 'Latvia', 'Lebanon', 'Lithuania', 'Macau', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique', 'Mauritius', 'Mexico', 'Moldova', 'Mongolia', 'Morocco', 'Mozambique', 'Myanmar', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Nigeria', 'Norfolk Island', 'North Macedonia', 'Norway', 'Oman', 'Pakistan', 'Panama', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Reunion', 'Romania', 'Russia', 'Rwanda', 'Saudi Arabia', 'Serbia', 'Singapore', 'Sint Maarten', 'Slovakia', 'Slovenia', 'South Africa', 'South Korea', 'Spain', 'Sri Lanka', 'Suriname', 'Sweden', 'Switzerland', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'U.K.', 'United States', 'U.S', 'Uzbekistan', 'Venezuela', 'Vietnam', 'Zimbabwe']

# Extract city info mentioned in the news text
city_info = extract_city_info(news_text, country_names)

# Create a DataFrame
df = pd.DataFrame(city_info, columns=["City", "Country", "Coordinates", "Range"])


df= df.drop_duplicates(subset="Coordinates")


# Create a map centered around the mean of latitude and longitude


def extract_lat_long(coord_str):
    # Split the coordinate string by space
    parts = coord_str.split()
    
    # Latitude is the first part until 'N' or 'S', Longitude is the second part until 'E' or 'W'
    lat = float(parts[0][:-1]) if parts[0][-1] in ['N', 'S'] else None
    long = float(parts[1][:-1]) if parts[1][-1] in ['E', 'W'] else None
    
    # Convert latitude and longitude to decimal degrees
    if lat is not None and long is not None:
        lat_decimal = lat if parts[0][-1] == 'N' else -lat
        long_decimal = long if parts[1][-1] == 'E' else -long
        return lat_decimal, long_decimal
    else:
        return None, None
    
# Define a function to extract the numeric part
def extract_numeric(value):
    if value.lower() == 'not specified':
        return 0
    else:
        # Split the string by space and take the first part
        numeric_part = value.split()[0]
        return numeric_part
    
# Apply the function to the Coordinates column
df[['Latitude', 'Longitude']] = df['Coordinates'].apply(lambda x: pd.Series(extract_lat_long(x)))
df['Range'] = df['Range'].apply(extract_numeric).astype(float)
    
#%%



m = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=2)
# Add markers for each city with a circle indicating range
for index, row in df.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=row['City'] + ', ' + row['Country'] + ', ' + row['Coordinates'] + ', ' + str(row["Range"]) +"km"
    ).add_to(m)
    folium.Circle(
        location=[row['Latitude'], row['Longitude']],
        radius=row['Range']*1000,  # in meters
        color='blue',
        fill=True,
        fill_opacity=0.15
    ).add_to(m)

# Save the map as an HTML file
m.save('map.html')


