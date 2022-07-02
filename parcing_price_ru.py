# Для парсинга нужно установить библиотеки BeautifulSoup и lxml

from bs4 import BeautifulSoup
import requests
import json


def parcing_price():
    # Задаем нужный нам url-адрес страницы, откуда берем информацию
    url = "https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.xml"

    # Далее сохраняем страницу к себе на компьютер, и открываем ее.
    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
    }

    req = requests.get(url, headers=headers)
    src = req.text

    with open("index_price_ru.xml", "w") as file:
        file.write(src)

    with open("index_price_ru.xml") as file:
        src = file.read()

    # На данном этапе подключаем библиотеку BeautifulSoup, которая позволяет парсить сайт
    soup = BeautifulSoup(src, "lxml")

    all_company = soup.find_all("row")
    company_name = dict()

    for item in all_company:
        if item.get("prevprice") is None:
            continue
        company_name[item.get("secid")] = [item.get("prevprice"), item.get("shortname")]

    # Сохраняем список в файл формата json и выводим на печать
    with open("company_price_ru.json", "w") as file:
        json.dump(company_name, file, indent=4, ensure_ascii=False)


with open("company_price_ru.json") as file:
    company_name = json.load(file)

# for items in company_name:
#     print(items)
# print(company_name)
