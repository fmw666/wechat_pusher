import requests
from bs4 import BeautifulSoup

url = "https://weather.com/zh-CN/weather/today/l/5a88f118aa4d4ed2e88e87e88f8a8986b20bbbbe8f0beabe18b7237697887197"

html = requests.get(url).text
bsObj = BeautifulSoup(html, "html.parser")

print(bsObj.select(".CurrentConditions--tempValue--3a50n")[0].text)
print(bsObj.select(".CurrentConditions--phraseValue--2Z18W")[0].text)
print(bsObj.select(".CurrentConditions--tempHiLoValue--3SUHy")[0].text)
