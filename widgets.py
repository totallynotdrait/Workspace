"""
Widgets
===============================
This Python script contains functions that creates a small window called widget.
The widget can be changed, modified and be interactive like quick note.
Some of this widgets like weather can get some information like your current city liviing,
but don't worry we will not use these information for anything else, you can check it btw.
"""
import dearpygui.dearpygui as dpg
from time import sleep


def widget_test():
    with dpg.window(label="Widget test", no_title_bar=True, no_collapse=True, width=150, height=150, no_resize=True, no_focus_on_appearing=True):
        dpg.add_text("hello")

def weather():
    global data, api_key, get_weather_data, g
    import requests, geocoder, threading



    g = geocoder.ip('me')
    city = g.city 

    def get_weather_data(api_key, city):  
        global api_url
        api_url = "http://api.openweathermap.org/data/2.5/weather"  
        params = {  
            "q": city_name,
            "units": "metric",  
            "appid": api_key  
        }  
        response = requests.get(api_url, params=params)  
        data = response.json()  
        return data  
    

    api_key = "93e79e1a26e4523a464c03e29805a4b5"  # CHANGE INTO NEW API KEY


    g = geocoder.ip('me')
    city_name = g.city

    thread = threading.Thread(target=lambda:get_weather_data(api_key, city_name), args=(), daemon=True)

    with dpg.window(label="weather", no_title_bar=True, no_collapse=True, width=250, height=250, no_resize=True, tag="wid_weather"):
        data = get_weather_data(api_key, city_name)
        print(data)
        
        dpg.add_text(city_name+f", {data.get('sys', {}).get('country')}\n")
        dpg.add_text(f"{data.get('main', {}).get('temp')}°C : Current temperature", tag="current_temp")
        dpg.add_text(f"{data.get('main', {}).get('temp_max')}°C : Maximum temperature", tag="max_temp")
        dpg.add_text(f"{data.get('main', {}).get('temp_min')}°C : Minimum temperature\n", tag="min_temp")
        dpg.add_text(f"{data.get('weather', [{}])[0].get('description', 'N/A')} : Sky status", tag="sky_stat")

    thread.start()


def quick_note():
    with dpg.window(label="quick note", no_title_bar=True, no_collapse=True, width=250, height=250, no_resize=True):
        dpg.add_input_text(multiline=True, height=-20, width=-1, tag="txt_content", tab_input=True)
        