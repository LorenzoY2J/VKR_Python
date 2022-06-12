# Для парсинга нужно установить библиотеки BeautifulSoup и lxml

from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import json

# Задаем нужный нам url-адрес страницы, откуда берем информацию
url = "https://porti.ru/search/stock?name=&p%5Bcountry%5D=0&exchange=NASDAQ&category=0&is_filled=on&p%5Bmarket_cap%5D=10%2C10000"

# Далее сохраняем страницу к себе на компьютер, и открываем ее.
headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
}

req = requests.get(url, headers=headers)
src = req.text

with open("index_usa.html", "w") as file:
    file.write(src)

with open("index_usa.html") as file:
    src = file.read()

# На данном этапе подключаем библиотеку BeautifulSoup, которая позволяет парсить сайт
soup = BeautifulSoup(src, "lxml")
all_company = soup.find_all(class_="sub")

# Создаем пустой список и теперь ищем тикеры по коду
company_tickers = []

all_category = soup.find_all("td", class_="center")

# Проходимся по полученным значениям, отбрасывая лишние символы, а также лишние значения
for item in all_category:
    company_tickers.append(item.text)

company_tickers = [line.strip() for line in company_tickers]

n, m = 9, 48

while n < len(company_tickers):
    del company_tickers[n:m]
    n += 9
    m += 9

# Создаем пустой словарь, в который с помощью проходу по коду и поиску нужных тегов, добавляем название компаний и
# их тикеры
company = {}
k, l = 0, 9

for item in all_company:
    companys = item.find("a")
    if companys is None:
        continue
    else:
        for i in companys:
            a = urlparse(companys.get("href")).path.replace('/company/NASDAQ:', '')
            company[a] = company_tickers[k:l]
            k += 9
            l += 9

# Сохраняем список в файл формата json и выводим на печать
with open("company_usa.json", "w") as file:
    json.dump(company, file, indent=4, ensure_ascii=False)

with open("company_usa.json") as file:
    all_company = json.load(file)

