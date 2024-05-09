import requests
# from urllib.request.Request
from bs4 import BeautifulSoup
import pandas as pd

url = "https://finance.naver.com/marketindex/"
response = requests.get(url)
# requests.get(), requests.post()
# response.text
soup = BeautifulSoup(response.text, "html.parser") 
# print(soup.prettify())

exchangeList = soup.select("#exchangeList > li")

exchange_data = []
baseurl = "https://finance.naver.com"

for item in exchangeList:
    data = {
        "title" : exchangeList[0].select_one(".h_lst").text,
        "exchange" : exchangeList[0].select_one(".value").text,
        "change" : exchangeList[0].select_one(".change").text,
        "updown" : exchangeList[0].select_one(".head_info.point_up > .blind").text,
        "link": baseurl + item.select_one("a").get("href")
    }
    exchange_data.append(data)
df = pd.DataFrame(exchange_data)
df.to_excel("./Web_data/naverfinance.xlsx")