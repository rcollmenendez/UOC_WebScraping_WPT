"""
@author: Ruben Coll Menendez
"""

"""
    Configurando el entorno
"""

import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

"""
    Inicio
"""

# Cargar la página con scroll infinito
driver = webdriver.Chrome(executable_path='C:/Users/RCOLL/Downloads/chromedriver_win32/chromedriver.exe')
driver.delete_all_cookies()
driver.get("https://www.worldpadeltour.com/jugadores?ranking=masculino")
time.sleep(2)
scroll_pause_time = 2
# Tamaño inicial de la página
screen_height = driver.execute_script("return window.screen.height;")
i = 1

while True:
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
    i += 1
    time.sleep(scroll_pause_time)
    # Capturamos la altura de la página
    scroll_height = driver.execute_script("return document.body.scrollHeight;")
    # Break the loop when the height we need to scroll to is larger than the total scroll height
    if (screen_height) * i > scroll_height:
        break

# Extraer URLS de los jugadores

'''
Una vez tenemos la página con todo el ranking de jugadores cargada,
procedemos a la extracción de las URLs de cada uno de ellos para, posteriormente,
cargar cada una de ellas y extraer la información individual de cada jugador
'''

soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

urls = []
for element in soup.find_all("li", {"class": "c-player-card__item"}):
    name = element.find("a", {"class": "c-trigger"})['href']
    urls.append(name)


# Comprobamos que se han cargado las URLs en la lista
print(len(urls))

# Limpiamos el entorno
del soup

"""
    Información Jugador
"""

# Abrir URL de cada jugador

driver = webdriver.Chrome(executable_path='C:/Users/RCOLL/Downloads/chromedriver_win32/chromedriver.exe')
driver.delete_all_cookies()
driver.get(urls[0])
content = driver.page_source
soup = BeautifulSoup(content,'html.parser')
driver.quit() # Force browser to quit when we have the data

# Extracción info
nombre = soup.find_all('h1',{'class': 'c-ranking-header__title'})[0].get_text()
ranking_actual = soup.find_all('p',{'class': 'c-ranking-header__data'})[0].get_text()
puntos = soup.find_all('p',{'class': 'c-ranking-header__data'})[1].get_text()
p_jugados = soup.find_all('p',{'class': 'c-ranking-header__data'})[2].get_text()
p_ganados = soup.find_all('p',{'class': 'c-ranking-header__data'})[3].get_text()
p_perdidos = soup.find_all('p',{'class': 'c-ranking-header__data'})[4].get_text()
efectividad = soup.find_all('p',{'class': 'c-ranking-header__data'})[5].get_text()
vict_consecutivas = soup.find_all('p',{'class': 'c-ranking-header__data'})[6].get_text()
url = urls[0] # Cambiar el 0 por el índice al hacer el loop

player_dict = {}

player_dict['nombre'] = nombre
player_dict['ranking_actual'] = ranking_actual
player_dict['puntos'] = puntos
player_dict['p_jugados'] = p_jugados
player_dict['p_ganados'] = p_ganados
player_dict['p_perdidos'] = p_perdidos
player_dict['efectividad'] = efectividad
player_dict['vict_consecutivas'] = vict_consecutivas
player_dict['url'] = url

print(player_dict)

# Diccionario a pandas df

df = pd.DataFrame(player_dict, index=[0])
df.head()

# Pandas df a CSV


