
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

# Chrome driver - Importante el path
driver = webdriver.Chrome(executable_path='C:/Users/RCOLL/Downloads/chromedriver_win32/chromedriver.exe')
# Abrimos la página con Chrome
driver.delete_all_cookies()
driver.get('https://www.worldpadeltour.com/jugadores/alejandro-galan-romo')
content = driver.page_source
soup = BeautifulSoup(content,'html.parser')
driver.quit() # Force browser to quit when we have the data

"""
results = []

for element in soup.find_all("div", {"class": "l-container l-container--data"}):
    name = element.find('div')
    results.append(name.text)

for x in results:
   print(x)
"""

# Definimos los valores que queremos extraer

'player_name' : {'tag': 'h1', 'class': 'c-ranking-header__title'}
soup.find_all('h1',{'class': 'c-ranking-header__title'})

'ranking' : {'tag': 'p', 'class': 'c-ranking-header__data'}
ranking = soup.find_all('p',{'class': 'c-ranking-header__data'})[0]
puntos = soup.find_all('p',{'class': 'c-ranking-header__data'})[1]
p_jugados = soup.find_all('p',{'class': 'c-ranking-header__data'})[2]
p_ganados = soup.find_all('p',{'class': 'c-ranking-header__data'})[3]
p_perdidos = soup.find_all('p',{'class': 'c-ranking-header__data'})[4]
efectividad = soup.find_all('p',{'class': 'c-ranking-header__data'})[5]
vict_consecutivas = soup.find_all('p',{'class': 'c-ranking-header__data'})[6]

# Datos personales y datos deportivos
soup.find_all('li',{'class': 'c-player__data-item'})

# Pandas dataframe

df = pd.DataFrame(data, columns = ['ranking', 'puntos', 'p_jugados'])