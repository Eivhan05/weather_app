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

def get_weather_data():
    global weatherstack_api, city
    city = searchbar.get().capitalize()
    response = requests.get(f"http://api.weatherstack.com/current?access_key={weatherstack_api}&query={city}")
    data = response.json()
    print(data)
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

# Get API key from environment variables
    weatherstack_api = os.environ.get('WEATHERSTACKAPI')

# weatherlist
    weatherlist = [["sunny", "clear"], ["cloudy", "overcast", "mist", "partly cloudy"], ["rain", "drizzle", "light rain", "rain Shower", "heavy rain", "moderate rain", "moderate or heavy rain shower"]]
# image size
    image_size = (200, 200)
    font = ctk.CTkFont( family="Montserrat", size=16)
# images
    clear_icon_day = ctk.CTkImage(dark_image=Image.open("weatherapp_icons/day_clear.png"), size=image_size)
    cloudy_icon_day = ctk.CTkImage(dark_image=Image.open("weatherapp_icons/day_partial_cloud.png"), size=image_size)
    rain_icon_day = ctk.CTkImage(dark_image=Image.open("weatherapp_icons/day_rain.png"), size=image_size)
    
    clear_icon_night = ctk.CTkImage(dark_image=Image.open("weatherapp_icons/night_clear.png"), size=image_size)
    cloudy_icon_night = ctk.CTkImage(dark_image=Image.open("weatherapp_icons/night_partial_cloud.png"), size=image_size)
    rain_icon_night = ctk.CTkImage(dark_image=Image.open("weatherapp_icons/night_rain.png"), size=image_size)

    transparent_icon = ctk.CTkImage(dark_image=Image.open("weatherapp_icons/transparent_image.png"), size=image_size)

                               
    icon_label = ctk.CTkLabel(root, text="")
    icon_label.grid(row=4, column=1, stick="w")

    grid_layout()

# design the window
    label = ctk.CTkLabel(root, text="Weather data:", font=font)
    label.grid(row=0, column=1, stick="w")


    search_button = ctk.CTkButton(root, text="Search", command=get_weather_data, font=font)
    search_button.grid(row=1, column=19)

    searchbar = ctk.CTkEntry(root, font=font)
    searchbar.grid(row=0, column=19)

    temperature_label = ctk.CTkLabel(root, text="", font=font)
    temperature_label.grid(row=1, column=1, sticky="W")

    feels_like_label = ctk.CTkLabel(root, text="", font=font)
    feels_like_label.grid(row=2, column=1, sticky="W")

    weather_type_label = ctk.CTkLabel(root, text="", font=font)
    weather_type_label.grid(row=3, column=1, sticky="W")

    root.mainloop()
    
