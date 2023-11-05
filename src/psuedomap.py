import folium
import requests  # To download the HTML file
import shutil
import csv


class InteractiveMap:
    def __init__(self, lat, lon, zoom_start):
        self.map = folium.Map(location=[lat, lon], zoom_start=zoom_start)
        self.tab1 = folium.FeatureGroup(name='Daytime')
        self.tab2 = folium.FeatureGroup(name='Nighttime')

        self.tile_layer1 = folium.TileLayer('CartoDB positron').add_to(self.tab1)
        self.tile_layer2 = folium.TileLayer('CartoDB dark_matter').add_to(self.tab2)

    def add_marker(self, marker_lat, marker_lon, noisy_gate, popup_text, tab=1):
        colors1 = [
          'darkred',  # 120+     noisy_gate = 0
          'red',      # 100-120  noisy_gate = 1
          'lightred', # 85-100   noisy_gate = 2
          'orange',   # 70-85    noisy_gate = 3
          'beige',    # 50-70    noisy_gate = 4
          'green'     # 0-50     noisy_gate = 5
          ]
        colors2 = [
          'beige',    # 55+      noisy_gate = 0
          'green',    # 55-40    noisy_gate = 1
          'blue',     # 40-30.   noisy_gate = 2
          'darkblue'  # 30-0     noisy_gate = 3
          ]

        if tab == 1:
            marker = folium.Marker([marker_lat, marker_lon], popup=folium.Popup(popup_text, max_width=300, min_width=300), icon=folium.Icon(color=colors1[noisy_gate]))
            marker.add_to(self.tab1)
        elif tab == 2:
            marker = folium.Marker([marker_lat, marker_lon], popup=folium.Popup(popup_text, max_width=300, min_width=300), icon=folium.Icon(color=colors2[noisy_gate]))
            marker.add_to(self.tab2)

    def save_map(self, filename):
        self.tab1.add_to(self.map)
        self.tab2.add_to(self.map)

        folium.LayerControl().add_to(self.map)
        self.map.save(filename)


class MyObject:
    def __init__(self, name, noise_type, lat, lon, noise, noisy_gate):
        self.name = name
        self.noise_type = noise_type
        self.lat = lat
        self.lon = lon
        self.noise = noise
        self.noisy_gate = noisy_gate


def create_objects_from_csv(file_path):
    objects1 = []
    objects2 = []

    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        # Skip the header row if it exists
        next(csv_reader)
        next(csv_reader)

        for row in csv_reader:
            # Assuming the CSV columns are in the order: attribute1, attribute2, attribute3
            name = row[1]
            noise_type = row[2]
            lat = float(row[3])
            lon = float(row[4])
            day_noise = float(row[5])
            night_noise = float(row[6])

            if (day_noise > 120):
              noisy_gate = 0
            elif (day_noise > 100):
              noisy_gate = 1
            elif (day_noise > 85):
              noisy_gate = 2
            elif (day_noise > 70):
              noisy_gate = 3
            elif (day_noise > 50):
              noisy_gate = 4
            else:
              noisy_gate = 5

            if (night_noise > 55):
              noisy_gate_night = 0
            elif (night_noise > 40):
              noisy_gate_night = 1
            elif (night_noise > 30):
              noisy_gate_night = 2
            else:
              noisy_gate_night = 3


            # Create an object using the row values
            obj1 = MyObject(name, noise_type, lat, lon, day_noise, noisy_gate)
            obj2 = MyObject(name, noise_type, lat, lon, night_noise, noisy_gate_night)
            objects1.append(obj1)
            objects2.append(obj2)

    return objects1, objects2

file_path = "" #input your own custom file path directory
objects1, objects2 = create_objects_from_csv(file_path)



# initialize recommendation mapping dictionaries
dict_daytime = {}
dict_nighttime = {}


# daytime
# 0-50 dB
dict_daytime[1] = ("Daytime Reference Noise:<br>" +
                   "normal breathing, whispering at 5 feet,  soft whisper<br><br>" +
                   "Daytime Tips:<br>" +
                   "This area is quiet and peaceful. Enjoy the tranquility and the softest sounds around you.")
# 50-70 dB
dict_daytime[2] = ("Daytime Reference Noise:<br>" +
                   "Rainfall, average room noise, background music<br><br>" +
                   "Daytime Tips:<br>" +
                   "The noise level is comparable to a calm and average room. It's a comfortable and soothing atmosphere.")
# 70-85 dB
dict_daytime[3] = ("Daytime Reference Noise:<br>" +
                   "Normal conversation, landscaping equipment (from inside a house), inside an airplane<br><br>" +
                   "Daytime Tips:<br>" + "It might be a bit noisy, but still manageable for most people.")
# 85-100 dB
dict_daytime[4] = ("Daytime Reference Noise:<br>" +
                   "Hairdryer, food processor, crowd rooster, approaching train<br><br>" +
                   "Daytime Tips:<br>" +
                   "This range represents moderately loud environments. It's a lively atmosphere, similar to being inside an airplane or a bustling city street.")
# 100-120 dB
dict_daytime[5] = ("Daytime Reference Noise:<br>" +
                   "Nightclubs and bars, ice cream trucks, dogs barking in ears, Rock or Pop concerts, siren<br><br>" +
                   "Daytime Tips:<br>" +
                   "It's a high-energy atmosphere where you might experience sounds like music, cheering, or applause. Take necessary precautions to protect your hearing in these situations.")
# 120+ dB
dict_daytime[6] = ("Daytime Reference Noise:<br>" +
                   "Jack-hammer, jet engine from 100 yards, gunshot<br><br>" +
                   "Daytime Tips:<br>" +
                   "This range represents extremely loud noises. It's important to exercise caution and protect your hearing in these environments. Prolonged exposure to these levels can be harmful to your hearing.")

# nighttime
# 0-30+
dict_nighttime[1] = ("Nighttime Reference Noise:<br>" +
                   "almost complete silence, faint nature sounds like rustling leaves or distant water trickling, gentle ticking of a clock or the soft hum of a fan in the background<br><br>" +
                     "Nighttime Tips:<br>" +
                   "It provides a quiet and serene environment that promotes restful sleep.")
# 30-40+
dict_nighttime[2] = ("Nighttime Reference Noise:<br>" +
                   "whisper or hushed conversation, light patter of raindrops on a windowpane, distant sound of a car passing by on a quiet street<br><br>" +
                   "Nighttime Tips:<br>" +
                   "While this noise level is generally acceptable for most individuals, it may not be suitable for more vulnerable groups such as children. Children are more sensitive to noise during sleep, so it's advisable to ensure a quieter environment for their well-being.\n")
# 40-55+
dict_nighttime[3] = ("Nighttime Reference Noise:<br>" +
                   "normal conversation at a moderate volume, the sound of a television playing at a reasonable volume, muffled street noise heard from inside a well-insulated room<br><br>" +
                   "Nighttime Tips:<br>" +
                   "Noise levels in this range can have adverse effects on health, particularly during sleep. Continuous exposure to such noise levels may disrupt sleep patterns, increase stress levels, and negatively impact overall well-being. It's important to minimize noise sources and create a more peaceful sleeping environment.\n")
# 55+
dict_nighttime[4] = ("Nighttime Reference Noise:<br>" +
                   "noisy neighbors talking loudly or playing music, traffic noise from a busy road or highway, construction work with heavy machinery operating nearby<br><br>" +
                   "Nighttime Tips:<br>" +
                   "Highly disturbed and can significantly disrupt sleep. Continuous exposure to high noise levels during the night can lead to sleep disturbances, insomnia, and potential health issues.\n")



def user_recommendation_message(MyObject, day):
  noise_type = MyObject.noise_type
  if day == 1:
    day_noise_level = MyObject.noise
    night_noise_level = 0
  elif day == 0:
    day_noise_level = 0
    night_noise_level = MyObject.noise

  #daytime message
  if(day_noise_level <= 50):
    day_message = str(round(day_noise_level, 2)) + "dB<br><br>"
    day_message += dict_daytime[1]
  elif (day_noise_level <= 70):
    day_message = str(round(day_noise_level, 2)) + "dB<br><br>"
    day_message += dict_daytime[2]
  elif (day_noise_level <= 85):
    day_message = str(round(day_noise_level, 2)) + "dB<br><br>"
    day_message += dict_daytime[3]
  elif (day_noise_level <= 100):
    day_message = str(round(day_noise_level, 2)) + "dB<br><br>"
    day_message += dict_daytime[4]
  elif (day_noise_level <= 120):
    day_message = str(round(day_noise_level, 2)) + "dB<br><br>"
    day_message += dict_daytime[5]
  else:
    day_message = str(round(day_noise_level, 2)) + "dB<br><br>"
    day_message += dict_daytime[6]
  #nighttime message
  if(night_noise_level <= 30):
    night_message = str(round(night_noise_level, 2)) + "dB<br><br>"
    night_message += dict_daytime[1]
  elif (night_noise_level <= 40):
    night_message = str(round(night_noise_level, 2)) + "dB<br><br>"
    night_message += dict_daytime[2]
  elif (night_noise_level <= 55):
    night_message = str(round(night_noise_level, 2)) + "dB<br><br>"
    night_message += dict_daytime[3]
  else:
    night_message = str(round(night_noise_level, 2)) + "dB<br><br>"
    night_message += dict_daytime[4]

  message = ["Noise type: " + noise_type + "<br><br>During the DAY (7AM - 11PM): " + day_message,
             "Noise type: " + noise_type + "<br><br>During the NIGHT (11PM - 7AM): " + night_message]
  if day == 1:
    return message[0]
  elif day == 0:
    return message[1]


    # TODO
    # def student_recommendation(self, sound_level):
    # def holidays_recommendation(self, sound_level):

my_map = InteractiveMap(43.65974555361324, 280.6028258800507, 15)  # Bahen coordinates -- initialize

for obj in objects1:
  my_map.add_marker(obj.lat, obj.lon, obj.noisy_gate, user_recommendation_message(obj, 1))

for obj in objects2:
  my_map.add_marker(obj.lat, obj.lon, obj.noisy_gate, user_recommendation_message(obj, 0), 2)


# Save the map to an HTML file
file_name = "interactive_map.html"  # Define the file name
my_map.save_map(file_name)

# Define the path to the directory where the file will be moved
save_directory = ""  #input custom directory path
target_file_path = f"{save_directory}/{file_name}"

# Move the file to the specified directory
shutil.move(file_name, target_file_path)

print(f"Map moved successfully to {target_file_path}")

