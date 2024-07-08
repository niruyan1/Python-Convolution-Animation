#%%
%clear
%reset -f
import re
import pandas as pd
import matplotlib.pyplot as plt
import simplekml
import math
plt.close("all")

def extract_radar_info_to_dataframe(file_path, countries):
    # Initialize an empty list to store dictionaries of data
    data = []
    
    # Open the text file for reading with specified encoding
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Check if the line starts with "Coordinates:"
            if line.startswith('Coordinates:'):
                coordinates = line.split(':')[1].strip()
                
                # Split the string by space to separate latitude and longitude parts
                parts = coordinates.split()
                latitude_str = parts[0]
                longitude_str = parts[1]
                # Extract numerical values and remove directional indicators
                latitude = float(latitude_str[:-1])  # Remove the last character ('N' or 'S') and convert to float
                longitude = float(longitude_str[:-1])  # Remove the last character ('E' or 'W') and convert to float
                # Adjust signs based on directional indicators
                if latitude_str.endswith('S'):
                    latitude = -latitude
                if longitude_str.endswith('W'):
                    longitude = -longitude
                
                # If no range, put default 400
                range_value = 400
                
                # Check the next line for "Range:"
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if next_line.startswith('Range:'):
                        range_value = next_line.split(':')[1].strip().split()[0]
                
                
                # Look for city and country information in preceding lines
                city = None
                country = None
                for j in range(i-1, -1, -1):
                    prev_line = lines[j].strip()
                    match = re.search(r',\s*({})\b'.format('|'.join(countries)), prev_line)
                    if match:
                        city = prev_line[:match.start()].strip()
                        if (city=="other radars are being prepared, for example in Austria" or city=="The July 30th, 2019 installation date noted on the WMO Radar Databa se page is likely when the page was updated in some way since four radars share that same date, in Japan" or city=="When updating our information for this radar site in August 2020, there appears to have been no data from this radar since September 23rd, 2017 based on looking through their archive here. The Friuli Venezia Giulia region site had data from other radars on their page. No range is shown on our map. They have a page with an interactive map of radar data here, with a loop here, that has data from Teolo (Monte Grande)" ):
                            continue
                        country = match.group().strip().lstrip(', ')
                        break

                # Append data as dictionary to the list
                data.append({'City': city,
                             'Country': country,
                             'Coordinates': coordinates, 
                             'Latitude': latitude, 
                             'Longitude': longitude, 
                             'Range': float(range_value)})
            
            i += 1
    
    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(data)
    
    # Reorder columns to have 'City' and 'Country' at the beginning
    if 'City' in df.columns and 'Country' in df.columns:
        cols = ['City', 'Country'] + [col for col in df.columns if col not in ['City', 'Country']]
        df = df[cols]
    
    return df

# Example usage:
file_path = 'C:/Users/niruy/Desktop/Google Maps Plotting/weatherRadars.txt'
country_names = ['Albania', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Bermuda', 'Botswana', 'Brazil', 'Brunei', 'Bulgaria', 'Cambodia', 'Canada', 'Cayman Islands', 'China', 'Colombia', 'Costa Rica', 'Croatia', 'Cuba', 'Curacao', 'Cyprus', 'Czechia', 'Denmark', 'Dominican Republic', 'Ecuador', 'El Salvador', 'Estonia', 'Fiji', 'Finland', 'France', 'French Guiana', 'Georgia', 'Germany', 'Greece', 'Guadeloupe', 'Guam', 'Guatemala', 'Guyana', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kuwait', 'Laos', 'Latvia', 'Lebanon', 'Lithuania', 'Macau', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique', 'Mauritius', 'Mexico', 'Moldova', 'Mongolia', 'Morocco', 'Mozambique', 'Myanmar', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Nigeria', 'Norfolk Island', 'North Macedonia', 'Norway', 'Oman', 'Pakistan', 'Panama', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Reunion', 'Réunion',  'Romania', 'Russia', 'Rwanda', 'Saudi Arabia', 'Serbia', 'Singapore', 'Sint Maarten', 'Slovakia', 'Slovenia', 'South Africa', 'South Korea', 'Spain', 'Sri Lanka', 'Suriname', 'Sweden', 'Switzerland', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'U.K', 'United States', 'U.S', 'Uzbekistan', 'Venezuela', 'Vietnam', 'Zimbabwe']
radar_df = extract_radar_info_to_dataframe(file_path, country_names)

radar_df.loc[radar_df['Coordinates'] == "29.198999N 48.033973E", ['City', 'Country']] = ["Unknown", "Kuwait"]
radar_df.loc[radar_df['Coordinates'] == "17.969803N 102.570129E", ['City', 'Country']] = ["Unknown", "Laos"]
radar_df.loc[radar_df['Coordinates'] == "33.763359N 35.557788E", ['City', 'Country']] = ["Unknown", "Lebanon"]
radar_df.loc[radar_df['Coordinates'] == "22.158758N 113.566366E", ['City', 'Country']] = ["Unknown", "Macau (China)"]
radar_df.loc[radar_df['Coordinates'] == "22.026578N 113.3704E", ['City', 'Country']] = ["Unknown", "Macau (China)"]
radar_df.loc[radar_df['Coordinates'] == "29.038287S 167.941397E", ['City', 'Country']] = ["Unknown", "Norfolk Island (Australia)"]
radar_df.loc[radar_df['Coordinates'] == "25.103654N 51.173395E", ['City', 'Country']] = ["Unknown", "Qatar"]
radar_df.loc[radar_df['Coordinates'] == "37.207617N 127.285879E", ['City', 'Country']] = ["Camp Humphreys", "South Korea"]
radar_df.loc[radar_df['Coordinates'] == "35.924217N 126.622082E", ['City', 'Country']] = ["Kunsan AFB", "South Korea"]
radar_df.loc[radar_df['Coordinates'] == "13.45592N 144.811078E", ['City', 'Country']] = ["Hagåtña (Andersen AFB)", "Guam (U.S.)"]



# Save the DataFrame to Excel
radar_df.to_excel('C:/Users/niruy/Desktop/Google Maps Plotting/weather_Radars.xlsx', index=False)


#%%
import pandas as pd
import math

def escape_xml_chars(text):
    """
    Replace special characters in XML with their escaped equivalents.
    """
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    return text

def create_kml_from_excel(input_file, output_file, blue_circle_countries):
    # Convert all countries in the list to lowercase for consistency
    blue_circle_countries = [country.lower() for country in blue_circle_countries]

    # Read Excel file into a pandas DataFrame
    df = pd.read_excel(input_file)

    # Initialize KML string
    kml_start = '<?xml version="1.0" encoding="UTF-8"?>\n'
    kml_start += '<kml xmlns="http://www.opengis.net/kml/2.2">\n'
    kml_start += '<Document>\n'

    # Define red circle style (red outline and red fill)
    kml_start += '<Style id="red_circle">\n'
    kml_start += '<LineStyle>\n'
    kml_start += '<color>ff0000ff</color>\n'  # Red color for the outline (RGBA format)
    kml_start += '<width>1</width>\n'
    kml_start += '</LineStyle>\n'
    kml_start += '<PolyStyle>\n'
    kml_start += '<color>1a0000ff</color>\n'  # 10% transparent blue fill (ARGB format)
    kml_start += '</PolyStyle>\n'
    kml_start += '</Style>\n'

    # Define blue circle style (blue outline and blue fill)
    kml_start += '<Style id="blue_circle">\n'
    kml_start += '<LineStyle>\n'
    kml_start += '<color>ffff0000</color>\n'  # Blue color for the outline (RGBA format)
    kml_start += '<width>1</width>\n'
    kml_start += '</LineStyle>\n'
    kml_start += '<PolyStyle>\n'
    kml_start += '<color>1aff0000</color>\n'  # 10% transparent red fill (ARGB format)
    kml_start += '</PolyStyle>\n'
    kml_start += '</Style>\n'

    # Iterate over rows in the DataFrame
    placemarks = ''
    for index, row in df.iterrows():
        city = escape_xml_chars(row['City'])  # Escape city name
        country = escape_xml_chars(row['Country'])  # Escape country name
        latitude = row['Latitude']
        longitude = row['Longitude']
        range_km = row['Range']  # Range in kilometers

        # Determine style based on country list
        if country.lower() in blue_circle_countries:
            style_id = 'blue_circle'  # Use blue circle style for Canada
        else:
            style_id = 'red_circle'   # Use red circle style for other countries

        # Convert range from kilometers to degrees (approximation)
        lat_deg_per_km = 1 / 111.32
        lon_deg_per_km = 1 / (111.32 * math.cos(math.radians(latitude)))

        # Calculate the number of points needed to approximate the circle
        min_num_points = 36  # Minimum 36 points for a circle
        num_points = max(min_num_points, int(360 * math.sqrt(range_km) / 100))

        # Generate polygon points for a circle
        points = []
        for i in range(num_points):
            angle = math.radians(float(i) / num_points * 360.0)
            dx = range_km * math.cos(angle)
            dy = range_km * math.sin(angle)
            point_longitude = longitude + (dx * lon_deg_per_km)
            point_latitude = latitude + (dy * lat_deg_per_km)
            points.append((point_longitude, point_latitude))

        # Ensure the first point is repeated at the end to close the polygon
        points.append(points[0])

        # Create Placemark for each city with a circle (polygon) and default yellow pin icon
        placemarks += '<Placemark>\n'
        placemarks += '<description><![CDATA[\n'
        placemarks += f'<b>City:</b> {city}<br>\n'
        placemarks += f'<b>Country:</b> {country}<br>\n'
        placemarks += f'<b>Range:</b> {range_km} km<br>\n'
        placemarks += f'<b>Latitude:</b> {latitude}<br>\n'
        placemarks += f'<b>Longitude:</b> {longitude}\n'
        placemarks += ']]></description>\n'
        placemarks += '<Point>\n'
        placemarks += f'<coordinates>{longitude},{latitude},0</coordinates>\n'  # Yellow pin coordinates
        placemarks += '</Point>\n'
        placemarks += '</Placemark>\n'

        # Add Placemark for the circle (polygon)
        placemarks += '<Placemark>\n'
        placemarks += f'<styleUrl>#{style_id}</styleUrl>\n'  # Link to appropriate style
        placemarks += '<Polygon>\n'
        placemarks += '<outerBoundaryIs>\n'
        placemarks += '<LinearRing>\n'
        placemarks += '<coordinates>\n'
        for point in points:
            placemarks += f'{point[0]},{point[1]},0\n'
        placemarks += '</coordinates>\n'
        placemarks += '</LinearRing>\n'
        placemarks += '</outerBoundaryIs>\n'
        placemarks += '</Polygon>\n'
        placemarks += '</Placemark>\n'

    # Construct complete KML content
    kml_end = '</Document>\n'
    kml_end += '</kml>\n'
    kml_content = kml_start + placemarks + kml_end

    # Write to output file with UTF-8 encoding
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(kml_content)

    print(f"KML file saved: {output_file}")

# Example usage:
input_excel = 'C:/Users/niruy/Desktop/Google Maps Plotting/weather_Radars.xlsx'  # Replace with your Excel file name
output_kml = 'C:/Users/niruy/Desktop/Google Maps Plotting/cities_with_pins_and_circles.kml'  # Name of the output KML file

# List of countries to have blue circles
blue_circle_countries = ['Canada']

create_kml_from_excel(input_excel, output_kml, blue_circle_countries)




#%%
df = pd.read_excel('weather_Radars.xlsx')
# Create an instance of Kml
kml = simplekml.Kml(open=1)

# Function to generate coordinates for a circle
def generate_circle_coords(center_lon, center_lat, radius_km, num_points=36):
    coords = []
    for i in range(num_points):
        angle = math.radians(float(i) / num_points * 360.0)
        dx = radius_km * math.cos(angle)
        dy = radius_km * math.sin(angle)
        lon = center_lon + (dx / (111.32 * math.cos(math.radians(center_lat))))
        lat = center_lat + (dy / 111.32)
        coords.append((lon, lat))
    coords.append(coords[0])  # Close the circle
    return coords

# Create a point for each city. The points' properties are assigned after the point is created
for index, row in df.iterrows():
    pnt = kml.newpoint()
    pnt.name = row['City'] + ', ' + row['Country']
    pnt.description = row['City'] + ', ' + row['Country'] + ', ' + row['Coordinates'] + ', ' + str(row["Range"]) +"km"
    pnt.coords = [(row['Longitude'], row['Latitude'])]
    
    # Create circle
    circle_coords = generate_circle_coords(row['Longitude'], row['Latitude'], row['Range'])
    pol = kml.newpolygon(name=row['City'] + ', ' + row['Country'] + ', ' + row['Coordinates'] + ', ' + str(row["Range"]) +"km", outerboundaryis=circle_coords)
    pol.style.linestyle.width = 2
    pol.style.polystyle.color = simplekml.Color.changealphaint(30, simplekml.Color.red)  # Blue color with 100 (fully opaque) alpha value

# Save the KML
kml.save("T00 Point.kml")