import customtkinter as ctk
import os
import requests
import matplotlib as plt
from PIL import Image
def create_window():
    global root
    root = ctk.CTk()
    root.title("weather app")
    root.geometry("600x400")
    ctk.set_appearance_mode("dark-blue")

def grid_layout():
    global row, column
    for i in range(20):
        root.rowconfigure(i, weight=1)
        root.columnconfigure(i, weight=1)

def main_layout():
    global icon_label, searchbar, temperature_label, feels_like_label, weather_type_label, favorite_locations_button, search_button, font
    
    
    icon_label = ctk.CTkLabel(root, text="")
    icon_label.grid(row=4, column=1, stick="w")

# design the window

    favorite_locations_button = ctk.CTkButton(root, text="Favorite Locations", command=favorite_locations_button_pressed, font=font)
    favorite_locations_button.grid(row=0, column=10)


    search_button = ctk.CTkButton(root, text="Search", command=search_button_pressed, font=font)
    search_button.grid(row=1, column=19)

    searchbar = ctk.CTkEntry(root, font=font)
    searchbar.grid(row=0, column=19)

    temperature_label = ctk.CTkLabel(root, text="", font=font)
    temperature_label.grid(row=1, column=1, sticky="W")

    feels_like_label = ctk.CTkLabel(root, text="", font=font)
    feels_like_label.grid(row=2, column=1, sticky="W")

    weather_type_label = ctk.CTkLabel(root, text="", font=font)
    weather_type_label.grid(row=3, column=1, sticky="W")

    return_button.destroy()
    for label in text_labels_favorite:
        label.destroy()
    for label in icon_labels_favorite:
        label.destroy()
    for label in temperature_labels_favorite:
        label.destroy()
    for button in remove_buttons:
        button.destroy()

def favorite_locations_button_pressed():
    global  weatherstack_api, favorites_list, return_button
# Get favorite locations from the saved file and storing it in favorites_list
    with open("favorites_data.txt", "r") as f_read:
            favorites_list = f_read.read().split()

#clear screen and display the favorite locations
    icon_label.destroy()
    weather_type_label.destroy()
    feels_like_label.destroy()
    temperature_label.destroy()
    favorite_locations_button.destroy()

    display_favorite_locations()

    search_button.configure(text="Add favorites", command=add_to_favorites_button_pressed, font=font)
    return_button = ctk.CTkButton(root, text="return", font=font, command=main_layout) 
    return_button.grid(row=0, column=13, stick="w")    
    

def add_to_favorites_button_pressed():
    global favorites_list, favorite_locations_button
    favorite_location = searchbar.get().capitalize()

    if len(favorites_list)>=3:
        print("Maximun number of favorites reached. Please remove one before adding a new one.")
    elif favorite_location in favorites_list:
        print("This location is already in your favorites.")
    else:
        with open("favorites_data.txt", "a") as file_w:
            file_w.write(f"{favorite_location} ")
            favorites_list.append(favorite_location)
    print(favorites_list)
    display_favorite_locations()


def display_favorite_locations():
    # function to display the favorite locations on the main screen
    global icon_label, weather_type_label, feels_like_label, temperature_label, font, text_label_favorite, icon_label_favorite, temperature_label_favorite
    i = 0
    for location in favorites_list:
        get_weather_data(location)
        # says the name of the location
        text_label_favorite = ctk.CTkLabel(root, text=f"{location}", font=font)
        text_label_favorite.grid(row=10, column=i, stick="nsew")
        text_labels_favorite.append(text_label_favorite)
        # create the weather icon
        icon_label_favorite = ctk.CTkLabel(root, text="")
        icon_label_favorite.grid(row=11, column=i, sticky="w")
        icon_labels_favorite.append(icon_label_favorite)
        # display the temperature
        temperature_label_favorite = ctk.CTkLabel(root, text=f"{data["current"]["temperature"]}°", font=font)
        temperature_label_favorite.grid(row=12, column=0+i, sticky="nsew")
        text_labels_favorite.append(temperature_label_favorite)
        #create remove button
        remove_button = ctk.CTkButton(root, text="Remove", font=font, command=lambda location=location: remove_favorite_button_pressed(location), hover_color="red")
        remove_button.grid(row=9, column=0+i, sticky="nsew")
        remove_buttons.append(remove_button)
        i += 1
        #configure the weather icon
        if data["current"]["weather_descriptions"][0].split(", ")[0].lower() in weatherlist[0] and data["current"]["is_day"] == "yes":
            icon_label_favorite.configure(image=clear_icon_day_favorites)

        elif data["current"]["weather_descriptions"][0].split(", ")[0].lower() in weatherlist[1] and data["current"]["is_day"] == "yes":
            icon_label_favorite.configure(image=cloudy_icon_day_favorites)
        
        elif data["current"]["weather_descriptions"][0].split(", ")[0].lower() in weatherlist[2] and data["current"]["is_day"] == "yes":
            icon_label_favorite.configure(image=rain_icon_day_favorites)

        elif data["current"]["weather_descriptions"][0].split(", ")[0].lower() in weatherlist[0] and data["current"]["is_day"] == "no":
                icon_label_favorite.configure(image=clear_icon_night_favorites)

        elif data["current"]["weather_descriptions"][0].split(", ")[0].lower() in weatherlist[1] and data["current"]["is_day"] == "no":
            icon_label_favorite.configure(image=cloudy_icon_night_favorites)

        elif data["current"]["weather_descriptions"][0].split(", ")[0].lower() in weatherlist[2] and data["current"]["is_day"] == "no":
            icon_label_favorite.configure(image=rain_icon_night_favorites)        
        else:
            icon_label_favorite.configure(image=transparent_icon_favorites)
        i += 1
def remove_favorite_button_pressed(location):
    print(location)
    if location in favorites_list:
        favorites_list.remove(location)
        with open("favorites_data.txt", "w") as file_w:
            file_w.write(" ".join(favorites_list))
        main_layout()
    
def search_button_pressed():
# Get the city name from the search bar and call the get_weather_data function and conigure_labels function
     city = searchbar.get().capitalize()
     get_weather_data(city)
     conigure_labels()
def get_weather_data(location):
# Fetching data from weatherstack API and storing it in data variable
    global weatherstack_api, data
    response = requests.get(f"http://api.weatherstack.com/current?access_key={weatherstack_api}&query={location}")
    data = response.json()

def conigure_labels():
     #funtion for configuring the labels on the main screen based on the data
    try:
        temperature_label.configure(text=f"Degrees celsius {data["current"]["temperature"]}°")
        weather_type_label.configure(text=data["current"]["weather_descriptions"][0].split(", ")[0])
        feels_like_label.configure(text=f"Feels like {data['current']['feelslike']}°")
    # day_conditionals
        if data["current"]["weather_descriptions"][0].split(", ")[0].lower() in weatherlist[0] and data["current"]["is_day"] == "yes":
            icon_label.configure(image=clear_icon_day)

        elif data["current"]["weather_descriptions"][0].split(", ")[0].lower() in weatherlist[1] and data["current"]["is_day"] == "yes":
            icon_label.configure(image=cloudy_icon_day)
        
        elif data["current"]["weather_descriptions"][0].split(", ")[0].lower() in weatherlist[2] and data["current"]["is_day"] == "yes":
            icon_label.configure(image=rain_icon_day)
# night_conditionals
        elif data["current"]["weather_descriptions"][0].split(", ")[0].lower() in weatherlist[0] and data["current"]["is_day"] == "no":
                icon_label.configure(image=clear_icon_night)

        elif data["current"]["weather_descriptions"][0].split(", ")[0].lower() in weatherlist[1] and data["current"]["is_day"] == "no":
            icon_label.configure(image=cloudy_icon_night)

        elif data["current"]["weather_descriptions"][0].split(", ")[0].lower() in weatherlist[2] and data["current"]["is_day"] == "no":
            icon_label.configure(image=rain_icon_night)        
        else:
            icon_label.configure(image=transparent_icon)


    except KeyError:
        temperature_label.configure(text="Location not found. Please try again.")
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    create_window()
    grid_layout()

# Get API key from environment variables
    weatherstack_api = os.environ.get('WEATHERSTACKAPI')

    weatherlist = [["sunny", "clear"], ["cloudy", "overcast", "overcast " "mist", "partly cloudy", "patchy rain nearby"], ["rain", "drizzle", "light rain", "rain Shower", "heavy rain", "moderate rain", "moderate or heavy rain shower"]]

    image_size = (200, 200)
    image_size_favorites = (100, 100)
    font = ctk.CTkFont( family="Montserrat", size=16)

# images
    clear_icon_day = ctk.CTkImage(dark_image=Image.open("weatherapp_icons/day_clear.png"), size=image_size)
    cloudy_icon_day = ctk.CTkImage(dark_image=Image.open("weatherapp_icons/day_partial_cloud.png"), size=image_size)
    rain_icon_day = ctk.CTkImage(dark_image=Image.open("weatherapp_icons/day_rain.png"), size=image_size)
    
    clear_icon_night = ctk.CTkImage(dark_image=Image.open("weatherapp_icons/night_clear.png"), size=image_size)
    cloudy_icon_night = ctk.CTkImage(dark_image=Image.open("weatherapp_icons/night_partial_cloud.png"), size=image_size)
    rain_icon_night = ctk.CTkImage(dark_image=Image.open("weatherapp_icons/night_rain.png"), size=image_size)

    clear_icon_day_favorites = ctk.CTkImage(dark_image=Image.open("weatherapp_icons/day_clear.png"), size=image_size_favorites)
    cloudy_icon_day_favorites = ctk.CTkImage(dark_image=Image.open("weatherapp_icons/day_partial_cloud.png"), size=image_size_favorites)
    rain_icon_day_favorites = ctk.CTkImage(dark_image=Image.open("weatherapp_icons/day_rain.png"), size=image_size_favorites)
    
    clear_icon_night_favorites = ctk.CTkImage(dark_image=Image.open("weatherapp_icons/night_clear.png"), size=image_size_favorites)
    cloudy_icon_night_favorites = ctk.CTkImage(dark_image=Image.open("weatherapp_icons/night_partial_cloud.png"), size=image_size_favorites)
    rain_icon_night_favorites = ctk.CTkImage(dark_image=Image.open("weatherapp_icons/night_rain.png"), size=image_size_favorites)

    transparent_icon = ctk.CTkImage(dark_image=Image.open("weatherapp_icons/transparent_image.png"), size=image_size)
    transparent_icon_favorites = ctk.CTkImage(dark_image=Image.open("weatherapp_icons/transparent_image.png"), size=image_size_favorites)

# just a placeholder button so the variables are defined
    return_button = ctk.CTkButton(root, text="")
    icon_label_favorite = ctk.CTkButton(root, text="")
    temperature_label_favorite = ctk.CTkButton(root, text="")
    text_label_favorite = ctk.CTkButton(root, text="")
    remove_button = ctk.CTkButton(root, text="")

    text_labels_favorite = []
    icon_labels_favorite = []
    temperature_labels_favorite = []
    remove_buttons = []

    main_layout()

    root.mainloop()
    
