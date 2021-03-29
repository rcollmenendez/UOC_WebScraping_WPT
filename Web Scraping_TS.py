from requests_html import HTMLSession
from bs4 import BeautifulSoup

# ------------------ URLs del Ranking ------------------
session = HTMLSession()
response = session.get('https://www.worldpadeltour.com/jugadores?ranking=todos')
soup = BeautifulSoup(response.content,"lxml")

urls = []
for element in soup.find_all("li", {"class": "c-player-card__item"}):
    name = element.find("a", {"class": "c-trigger"})['href']
    urls.append(name)

for x in urls:
   print(x)






