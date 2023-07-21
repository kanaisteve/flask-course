# Tutorial 1: How to Build a Weather App with Python | Weather API

`$ pip install requests`

By the end, your project layout will look like this:
```
/home/user/Projects/weather-app
|-- app.py
```

```
import requests

open_weather_api_key = 'e426b567ec444734de92d734eaa00764'

user_input = input("Enter city: ")

weather_data = requests.get(
    f"https://api.openweathermap.org/data/2.5/weather?q={user_input}&units=imperial&APPID={open_weather_api_key}")

if weather_data.json()['cod'] == '404':
    print("No City Found")
else:
    print(weather_data.status_code)
    print(weather_data.json())
    
    weather = weather_data.json()['weather'][0]['main']
    temp = round(weather_data.json()['main']['temp'])

    print(f"The weather in {user_input} is: {weather}")
    print(f"The temperature in {user_input} is {weather}")
```

```
Enter city: Lusaka
200
{'coord': {'lon': 28.2871, 'lat': -15.4067}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 62.85, 'feels_like': 61.61, 'temp_min': 62.85, 'temp_max': 62.85, 'pressure': 1030, 'humidity': 59}, 'visibility': 10000, 'wind': {'speed': 21.85, 'deg': 110}, 'clouds': {'all': 75}, 'dt': 1688718861, 'sys': {'type': 1, 'id': 2113, 'country': 'ZM', 'sunrise': 1688704447, 'sunset': 1688744932}, 'timezone': 7200, 'id': 909137, 'name': 'Lusaka', 'cod': 200}
The weather in Lusaka is: Clouds
The temperature in Lusaka is Clouds
```

## References
1. [How to Build a Weather App with Python | Weather API - YouTube](https://www.youtube.com/watch?v=baWzHKfrvqw)