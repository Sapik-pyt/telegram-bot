import requests
import datetime


def get_weather(city, open_weather_token):
    code_smile =  {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    res = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"   #&units=metric метрическая система
    )
    data = res.json()
    city = data['name']
    cur_weather = data['main']['temp']
    humidity = data['main']['humidity']
    pressure = data['main']['pressure']
    speed_wind = data['wind']['speed']
    description = data['weather'][0]['main']
    if description in code_smile:
        x = code_smile[description]
    else:
        x = 'Выгляни в окно'
    sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
    sunset_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunset'])# формируем формат времени из unix в обычный
    lenght_of_the_day = sunset_timestamp - sunrise_timestamp

    return (f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***"
              f"Погода в городе: {city}\nТемпература: {cur_weather}C°\n"
              f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {speed_wind} м/с\n"
              f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {lenght_of_the_day}\n"
              f"Описание погоды: {x}\nХорошего дня!"
            )   