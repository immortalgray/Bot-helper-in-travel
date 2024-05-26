import requests
from config import API_KEY


def weather(city):
    # URL API сервиса OpenWeatherMap
    url = 'https://api.openweathermap.org/data/2.5/weather'

    # Параметры запроса к API (например, название города и API ключ)
    params = {
        'q': city,
        'type': 'like',  # Название города
        'units': 'metric',
        'lang': "ru",
        'appid': API_KEY  # Замените 'your_api_key_here' на ваш API ключ
    }

    # Выполняем GET-запрос к API
    response = requests.get(url, params=params)

    # Проверяем успешность запроса
    if response.status_code == 200:
        # Если запрос успешен, выводим полученные данные (например, в формате JSON)
        weather_data = response.json()
        description = f"На улице: {weather_data['weather'][0]['description']}"
        main_temp = f"Средняя температура:, {int(weather_data['main']['temp'])}°C"
        humidity = f"Влажность: {weather_data["main"]["humidity"]}%"
        return True, description, main_temp, humidity
    else:
        # Если возникла ошибка, выводим сообщение об ошибке
        return False, f'Ошибка получения данных: {response.status_code}', None, None

def only_temp(city):
    url = 'https://api.openweathermap.org/data/2.5/weather'

    # Параметры запроса к API (например, название города и API ключ)
    params = {
        'q': city,
        'type': 'like',  # Название города
        'units': 'metric',
        'lang': "ru",
        'appid': API_KEY  # Замените 'your_api_key_here' на ваш API ключ
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        # Если запрос успешен, выводим полученные данные (например, в формате JSON)
        weather_data = response.json()
        main_temp = f"{int(weather_data['main']['temp'])}°C"
        return True, main_temp
    else:
        return False, f'Ошибка получения данных: {response.status_code}', None, None