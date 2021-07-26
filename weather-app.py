import tkinter
import requests
import json
from configparser import ConfigParser
import tkinter.messagebox as tkMessageBox
import time
#========================Initialization========================
window=tkinter.Tk()

config_file="config.ini"
config=ConfigParser()
config.read(config_file)
api_key= config["api_key"]["key"]


#========================Variables========================
city=tkinter.StringVar()

weather_image=""
#search_image=tkinter.PhotoImage(file="images/search.png")

#========================Functions========================
def get_weather(city):
    api_request = requests.get("https://api.openweathermap.org/data/2.5/weather?q="
                               + city + "&units=metric&appid="+api_key)
    api = json.loads(api_request.content)
    if api:
        city=api["name"]
        country=api["sys"]["country"]
        temp_kelvin=api["main"]["temp"]
        temp_celsius=int(temp_kelvin-273.15)
        temp_farenheit=(temp_celsius)*9/5+32
        icon= api["weather"][0]["icon"]
        weather=api["weather"][0]["description"]
        min_temp=int(api["main"]["temp_min"]-273.15)
        max_temp=int(api["main"]["temp_max"]-273.15)
        pressure=api["main"]["pressure"]
        humidity=api["main"]["humidity"]
        wind=api["wind"]["speed"]
        sunrise=time.strftime("%I:%M:%S",time.gmtime(api["sys"]["sunrise"]))
        sunset=time.strftime("%I:%M:%S",time.gmtime(api["sys"]["sunset"]))
        data=(city, country, temp_celsius, icon, weather, min_temp, max_temp, pressure, humidity, wind, sunrise, sunset)
        return data

    else:
        return None


def search():
    weather_data=get_weather(city.get())
    if weather_data:
        location_label["text"]="{}, {}".format(weather_data[0], weather_data[1])
        temperature_label["text"]="{}K".format(weather_data[2])
        canvas_label["image"]=tkinter.PhotoImage(file="images/{}.png".format(weather_data[3]))
        description_label["text"]=weather_data[4]
        min_temp_value_label["text"]=weather_data[5]
        max_temp_value_label["text"]=weather_data[6]
        pressure_value_label["text"]=weather_data[7]
        humidity_value_label["text"]=weather_data[8]
        
        
        #wind_value_label["text"]=weather_data[9]
        sunrise_value_label["text"]=weather_data[10]
        sunset_value_label["text"]=weather_data[11]
    else:
        tkMessageBox.showerror("Error","Cannot fint {} city".format(city.get()))

#========================Window-config========================
window.geometry("300x400")
window.title("Weather App")
window.resizable(False,False)

#========================Widgets========================
top_frame=tkinter.Frame(window)
top_frame.pack(side=tkinter.TOP)

city_label=tkinter.Label(top_frame, text="City")
city_label.grid(row=0,column=0,padx=10, pady=10)

city_entry=tkinter.Entry(top_frame, textvariable=city, width=25)
city_entry.grid(row=0,column=1, padx=10)

city_button=tkinter.Button(top_frame, text="Search", command=search)
city_button.grid(row=0,column=2)

location_label=tkinter.Label(window, text="Location", font=("bold",20))
location_label.pack()

temperature_label=tkinter.Label(window, text="Temperature", font=("bold",40))
temperature_label.pack()

canvas_label=tkinter.Label(window, image=weather_image)
canvas_label.pack()

description_label=tkinter.Label(window, text="Description", font=("bold",20))
description_label.pack()

bottom_frame=tkinter.Frame(window)
bottom_frame.pack(side=tkinter.BOTTOM)

min_temp_label=tkinter.Label(bottom_frame, text="Min Temp:")
min_temp_label.grid(row=0, column=0, padx=10)

min_temp_value_label=tkinter.Label(bottom_frame, text=" ")
min_temp_value_label.grid(row=0, column=1, padx=10)

max_temp_label=tkinter.Label(bottom_frame, text="Max Temp:")
max_temp_label.grid(row=0, column=2, padx=10)

max_temp_value_label=tkinter.Label(bottom_frame, text=" ")
max_temp_value_label.grid(row=0, column=3, padx=10)

pressure_label=tkinter.Label(bottom_frame, text="Pressure:")
pressure_label.grid(row=1, column=0, padx=10)

pressure_value_label=tkinter.Label(bottom_frame, text=" ")
pressure_value_label.grid(row=1, column=1, padx=10)

humidity_label=tkinter.Label(bottom_frame, text="Humidity:")
humidity_label.grid(row=1, column=2, padx=10)

humidity_value_label=tkinter.Label(bottom_frame, text=" ")
humidity_value_label.grid(row=1, column=3, padx=10)

sunrise_label=tkinter.Label(bottom_frame, text="Sunrise:")
sunrise_label.grid(row=2, column=0, padx=10)

sunrise_value_label=tkinter.Label(bottom_frame, text=" ")
sunrise_value_label.grid(row=2, column=1, padx=10)

sunset_label=tkinter.Label(bottom_frame, text="Sunset:")
sunset_label.grid(row=2, column=2, padx=10)

sunset_value_label=tkinter.Label(bottom_frame, text=" ")
sunset_value_label.grid(row=2, column=3, padx=10)

credits_frame=tkinter.Frame(window)
credits_frame.pack()



window.mainloop()
