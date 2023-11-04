import folium
import requests  # To download the HTML file

class InteractiveMap:
    def __init__(self, lat, lon, zoom_start):
        self.map = folium.Map(location=[lat, lon], zoom_start=zoom_start)

    def add_marker(self, marker_lat, marker_lon, popup_text):
        folium.Marker([marker_lat, marker_lon], popup=popup_text).add_to(self.map)

    def save_map(self, filename):
        self.map.save(filename)


my_map = InteractiveMap(51.5074, -0.1278, 10)  # London coordinates

# Adding markers to the map
my_map.add_marker(51.5033, -0.1195, "Buckingham Palace")
my_map.add_marker(51.5007, -0.1246, "Big Ben")

# Save the map to an HTML file
file_name = "interactive_map.html"  # Define the file name
my_map.save_map(file_name)

# Define the path to the directory where the file will be moved
save_directory = "/Users/jessica/Desktop/NewHacks2023"
target_file_path = f"{save_directory}/{file_name}"

# Move the file to the specified directory
shutil.move(file_name, target_file_path)

print(f"Map moved successfully to {target_file_path}")

