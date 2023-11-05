import folium
import requests  # To download the HTML file
import shutil
import csv


class InteractiveMap:
    def __init__(self, lat, lon, zoom_start):
        self.map = folium.Map(location=[lat, lon], zoom_start=zoom_start)

    def add_marker(self, marker_lat, marker_lon, noisy_gate, popup_text):
        colors = [
          'darkred',  #120+     noisy_gate = 0
          'red',      #100-120  noisy_gate = 1
          'lightred', #85-100   noisy_gate = 2
          'orange',   #70-85    noisy_gate = 3
          'beige',    #50-70    noisy_gate = 4
          'green'     #0-50     noisy_gate = 5
          ]
        folium.Marker([marker_lat, marker_lon], popup=popup_text, icon=folium.Icon(color=colors[noisy_gate])).add_to(self.map)

    def save_map(self, filename):
        self.map.save(filename)

class MyObject:
    def __init__(self, name, noise_type, lat, lon, NL_min, NL_max, NL_avg):
        self.name = name
        self.noise_type = noise_type
        self.lat = lat
        self.lon = lon
        self.NL_min = NL_min
        self.NL_max = NL_max
        self.NL_avg = NL_avg


def create_objects_from_csv(file_path):
    objects = []

    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        # Skip the header row if it exists
        next(csv_reader)

        for row in csv_reader:
            # Assuming the CSV columns are in the order: attribute1, attribute2, attribute3
            name = row[0]
            noise_type = row[1]
            lat = row[2]
            lon = row[3]
            NL_min = row[4]
            NL_max = row[5]
            NL_avg = row[6]

            # Create an object using the row values
            obj = MyObject(name, noise_type, lat, lon, NL_min, NL_max, NL_avg)
            objects.append(obj)
    return objects


# initialize recommendation mapping dictionaries
dict_daytime = {}
dict_nighttime = {}

# daytime
# 0-50 dB
dict_daytime[1] = ("Daytime Reference Noise:\n" +
                   "normal breathing, whispering at 5 feet,  soft whisper\n" +
                   "Daytime Tips:\n" +
                   "This area is quiet and peaceful. Enjoy the tranquility and the softest sounds around you.\n")
# 50-70 dB
dict_daytime[2] = ("Daytime Reference Noise:\n" +
                   "Rainfall, average room noise, background music\n" +
                   "Daytime Tips:\n" +
                   "The noise level is comparable to a calm and average room. It's a comfortable and soothing atmosphere.\n")
# 70-85 dB
dict_daytime[3] = ("Daytime Reference Noise:\n" +
                   "Normal conversation, landscaping equipment (from inside a house), inside an airplane\n" +
                   "Daytime Tips:\n" + "It might be a bit noisy, but still manageable for most people.\n")
# 85-100 dB
dict_daytime[4] = ("Daytime Reference Noise:\n" +
                   "Hairdryer, food processor, crowd rooster, approaching train\n" +
                   "Daytime Tips:\n" +
                   "This range represents moderately loud environments. It's a lively atmosphere, similar to being inside an airplane or a bustling city street.\n")
# 100-120 dB
dict_daytime[5] = ("Daytime Reference Noise:\n" +
                   "Nightclubs and bars, ice cream trucks, dogs barking in ears, Rock or Pop concerts, siren\n" +
                   "Daytime Tips:\n" +
                   "It's a high-energy atmosphere where you might experience sounds like music, cheering, or applause. Take necessary precautions to protect your hearing in these situations.\n")
# 120+ dB
dict_daytime[6] = ("Daytime Reference Noise:\n" +
                   "Jack-hammer, jet engine from 100 yards, gunshot\n" +
                   "Daytime Tips:\n" +
                   "This range represents extremely loud noises. It's important to exercise caution and protect your hearing in these environments. Prolonged exposure to these levels can be harmful to your hearing.\n")

# nighttime
# 0-30+
dict_nighttime[1] = ("Nighttime Reference Noise:\n" +
                   "almost complete silence, faint nature sounds like rustling leaves or distant water trickling, gentle ticking of a clock or the soft hum of a fan in the background\n" +
                     "Nighttime Tips:\n" +
                   "It provides a quiet and serene environment that promotes restful sleep.\n")
# 30-40+
dict_nighttime[2] = ("Nighttime Reference Noise:\n" +
                   "whisper or hushed conversation, light patter of raindrops on a windowpane, distant sound of a car passing by on a quiet street\n" +
                   "Nighttime Tips:\n" +
                   "While this noise level is generally acceptable for most individuals, it may not be suitable for more vulnerable groups such as children. Children are more sensitive to noise during sleep, so it's advisable to ensure a quieter environment for their well-being.\n")
# 40-55+
dict_nighttime[3] = ("Nighttime Reference Noise:\n" +
                   "normal conversation at a moderate volume, the sound of a television playing at a reasonable volume, muffled street noise heard from inside a well-insulated room\n" +
                   "Nighttime Tips:\n" +
                   "Noise levels in this range can have adverse effects on health, particularly during sleep. Continuous exposure to such noise levels may disrupt sleep patterns, increase stress levels, and negatively impact overall well-being. It's important to minimize noise sources and create a more peaceful sleeping environment.\n")
# 55+
dict_nighttime[4] = ("Nighttime Reference Noise:\n" +
                   "noisy neighbors talking loudly or playing music, traffic noise from a busy road or highway, construction work with heavy machinery operating nearby\n" +
                   "Nighttime Tips:\n" +
                   "Highly disturbed and can significantly disrupt sleep. Continuous exposure to high noise levels during the night can lead to sleep disturbances, insomnia, and potential health issues.\n")


def user_recommendation_message(MyObject):
  noise_type = MyObject.noise_type
  day_noise_level = MyObject.day_noise_level
  night_noise_level = MyObject.night_night_level
  message = ""
  day_message = ""
  night_message = ""
  #daytime message
  if(day_noise_level <= 50):
    day_message = day_noise_level + "\n"
    day_message += dict_daytime[1]
  elif (day_noise_level <= 70):
    day_message = day_noise_level + "\n"
    day_message += dict_daytime[2]
  elif (day_noise_level <= 85):
    day_message = day_noise_level + "\n"
    day_message += dict_daytime[3]
  elif (day_noise_level <= 100):
    day_message = day_noise_level + "\n"
    day_message += dict_daytime[4]
  elif (day_noise_level <= 120):
    day_message = day_noise_level + "\n"
    day_message += dict_daytime[5]
  else:
    day_message = day_noise_level + "\n"
    day_message += dict_daytime[6]
  #nighttime message
  if(night_noise_level <= 30):
    night_message = night_noise_level + "\n"
    night_message += dict_daytime[1]
  elif (night_noise_level <= 40):
    night_message = night_noise_level + "\n"
    night_message += dict_daytime[2]
  elif (night_noise_level <= 55):
    night_message = night_noise_level + "\n"
    night_message += dict_daytime[3]
  else:
    night_message = night_noise_level + "\n"
    night_message += dict_daytime[4]

  message = "Noise type: " + noise_type + "\nDuring the DAY (7AM - 11PM): " + day_message + "\nDuring the NIGHT (11PM - 7AM): " + night_message
  return message


    # TODO
    # def student_recommendation(self, sound_level):
    # def holidays_recommendation(self, sound_level):


my_map = InteractiveMap(51.5074, -0.1278, 10)  # London coordinates

# Adding markers to the map
my_map.add_marker(51.5033, -0.1195, "Buckingham Palace")
my_map.add_marker(51.5007, -0.1246, "Big Ben")

# Save the map to an HTML file
file_name = "interactive_map.html"  # Define the file name
my_map.save_map(file_name)

# Define the path to the directory where the file will be moved
save_directory = ""  #input custom directory path
target_file_path = f"{save_directory}/{file_name}"

# Move the file to the specified directory
shutil.move(file_name, target_file_path)

print(f"Map moved successfully to {target_file_path}")

