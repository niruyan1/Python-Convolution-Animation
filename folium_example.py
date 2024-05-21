import folium

# Example data: latitude, longitude, and some information
data = [
    {'lat': 40.7128, 'lon': -74.0060, 'info': 'New York City'},
    {'lat': 34.0522, 'lon': -118.2437, 'info': 'Los Angeles'},
    {'lat': 41.8781, 'lon': -87.6298, 'info': 'Chicago'},
    {'lat': 29.7604, 'lon': -95.3698, 'info': 'Houston'},
    {'lat': 33.4484, 'lon': -112.0740, 'info': 'Phoenix'}
]

# Create a folium map centered around the mean coordinates of the data
map = folium.Map(location=[sum(d['lat'] for d in data)/len(data), 
                           sum(d['lon'] for d in data)/len(data)], 
                 zoom_start=4)

# Add markers for each data point
for d in data:
    folium.Marker(location=[d['lat'], d['lon']], popup=d['info']).add_to(map)

# Save the map as an HTML file
map.save('map.html')