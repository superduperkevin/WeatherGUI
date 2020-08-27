from tkinter import *
from tkinter import messagebox
from tkinter import ttk #css for tkinter 
from configparser import ConfigParser

# import io
# import urllib.request
# import base64
import time

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import requests

weather_url = 'http://api.openweathermap.org/data/2.5/weather?q={},{}&appid={}'

bg_url = 'https://api.unsplash.com/search/photos?query={}&client_id={}'


config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
weather_api_key = config['weather_api_key']['key']
unsplash_access_key = config['unsplash_api_key']['access_key']


def get_image(city): 
    image_index = 0
    result = requests.get(bg_url.format(city, unsplash_access_key))
    if result: 
        json = result.json()
        first_url = json['results'][image_index]['urls']['raw']
        return first_url
        u = urllib.request.urlopen(first_url)
        image_byt = u.read()
        u.close()
        # photo = PhotoImage(data=base64.encodestring(image_byt))
        # return photo
    else:
        return None


def get_weather(city, country): 
    result = requests.get(weather_url.format(city, country, weather_api_key))
    if result:
        json = result.json()
        # (City, Country, temp_celsius, temp_fahrenheit, icon, weather)
        city = json['name']
        country = json['sys']['country']
        temp_kelvin = json['main']['temp']
        temp_celsius = temp_kelvin - 273.15
        temp_fahrenheit = temp_celsius * 9/5 + 32
        icon = json['weather'][0]['icon']
        weather = json['weather'][0]['main']
        final = (city, country, temp_celsius, temp_fahrenheit, icon, weather)
        return final
    else:
        return None


def search():
    city = city_text.get()
    country = country_text.get()
    weather = get_weather(city, country)
    photo = get_image(city)
    if weather and city and country: 
        location_lbl['text'] = '{}, {}'.format(weather[0], weather[1])
        image['bitmap'] = 'weather_icons/{}.png'.format(weather[4])
        weather_lbl['text'] = weather[5]
        temp_lbl['text'] = '{:.2f}°C \n {:.2f}°F'.format(weather[2], weather[3])
        url_lbl['text'] = photo

    elif not city or not country: 
        messagebox.showerror('Error', 'Cannot find city: {} in country: {}'.format(city, country))
    else: 
        messagebox.showerror('Error', 'Error Occured')


app = Tk()
app.title("Weather App")
app.geometry('900x700')

# city_image = Tk()

#Top Frame
top_frame = LabelFrame(app, text='Search', padx=50, pady=5)
top_frame.pack(side='top',padx=10, pady=10)

##Search Field
city_text = StringVar()
city_entry = ttk.Entry(top_frame, textvariable=city_text)
city_entry.pack(pady=2)

##Country Field
country_text = StringVar()
country_entry = ttk.Entry(top_frame, textvariable=country_text)
country_entry.pack(pady=2)

##Search Button
search_btn = ttk.Button(top_frame, text="Search by City, Country", width=20, command=search)
search_btn.pack(pady=10)

#Bottom Frame
bottom_frame = LabelFrame(app, text='Details', height=500, padx=100, pady=5)
bottom_frame.pack(side='top', padx=10, pady=10)

##Location
location_lbl = ttk.Label(bottom_frame, text='--', font=('bold', 20))
location_lbl.pack()

##Image
image = Label(bottom_frame, bitmap='--', relief='sunken')
image.pack(pady=10)

##Weather
weather_lbl = ttk.Label(bottom_frame, text='--')
weather_lbl.pack()

##Temperature
temp_lbl = ttk.Label(bottom_frame, text='--', font=('bold', 30))
temp_lbl.pack(padx=10, pady=10)

url_lbl = ttk.Label(bottom_frame, text='--')
url_lbl.pack(padx=10, pady=10)

#Bottom Frame
def bottom():
    statusbar = ttk.Label(app, text='Application Opened: {}'.format(time.asctime(time.localtime())), relief='sunken', anchor='w', font=('Italic', 15))
    statusbar.pack(side='bottom', fill='x')
bottom()

app.mainloop()  