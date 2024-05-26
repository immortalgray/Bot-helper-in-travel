import requests
from bs4 import BeautifulSoup as BeSu
import logging


logging.basicConfig(filename="log.txt", level=logging.ERROR, format="%(asctime)s FILE: %(filename)s IN: %(funcName)s MESSAGE: %(message)s", filemode="w")


def city_pic(city):
    try:
        response = requests.get(f"https://ru.wikipedia.org//wiki/{city}")
        html = BeSu(response.content, "html.parser")
        image = html.find('table', class_='infobox').find("td", class_='infobox-image').find('a')
        return True, 'https://ru.wikipedia.org/' + image['href']
    except Exception as e:
        logging.error(e)
        return False, "Картинка не найдена или написан неправильно город"