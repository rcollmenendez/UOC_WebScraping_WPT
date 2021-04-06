"""
Estudios: Máster universitario de Ciencia de Datos de la UOC
Asignatura: (M2.851) Tipología y ciclo de vida de los datos - Aula 3
Actividad: Práctica 1 - Web Scraping
Estudiante: Rubén Coll Menéndez
"""

# -------------------------------
# Configurando el entorno
# -------------------------------

import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import random


# -------------------------------
# Inicio
# -------------------------------

# Cargar la página con scroll infinito
driver = webdriver.Chrome(executable_path='C:/Users/RCOLL/Downloads/chromedriver_win32/chromedriver.exe')
driver.delete_all_cookies()
driver.get('https://www.worldpadeltour.com/jugadores?ranking=masculino') # Descargar ranking masculino
# driver.get("https://www.worldpadeltour.com/jugadores?ranking=femenino") # Descargar ranking femenino

time.sleep(2)
scroll_pause_time = 2
screen_height = driver.execute_script('return window.screen.height;')
i = 1
while True:
    driver.execute_script('window.scrollTo(0, {screen_height}*{i});'.format(screen_height=screen_height, i=i))
    i += 1
    time.sleep(scroll_pause_time)
    scroll_height = driver.execute_script('return document.body.scrollHeight;')
    if (screen_height) * i > scroll_height:
        break

# -------------------------------
# Extracción URLs de cada jugador
# -------------------------------

'''
Una vez tenemos la página con todo el ranking de jugadores cargada,
procedemos a la extracción de las URLs de cada uno de ellos para, posteriormente,
cargar cada una de ellas y extraer la información individual de cada jugador
'''

soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()

# Creamos una lista vacía e insertamos las URLs del código HTML
urls = []
for element in soup.find_all('li', {'class': 'c-player-card__item'}):
    name = element.find('a', {'class': 'c-trigger'})['href']
    urls.append(name)

soup.find_all('p', {'class': 'c-form__group'})

# Comprobamos que se han cargado las URLs en la lista
len(urls)

# Limpiamos las variables que ya no vamos a necesitar
del soup

# -------------------------------
# Extracción información de cada jugador
# -------------------------------

'''
Una vez tenemos todas las URLs que nos dirigen a las fichas de cada uno de los jugadores,
el paso 3 consiste en la extracción de la información de cada uno de ellos.
'''

# Creamos un diccionario vacío en el que insertaremos la info
player_dict = {'nombre': [],
               'ranking_actual': [],
               'puntos_wpt': [],
               'p_jugados': [],
               'p_ganados': [],
               'p_perdidos': [],
               'efectividad': [],
               'vict_consecutivas': [],
               'url': []}

# Creamos una lista vacía para comprobar que urls se han escaneado
scanned_urls = []

for url in urls[0:30]:
    scanned_urls.append(url)
    # Abrir URL de cada jugador
    driver = webdriver.Chrome(executable_path='C:/Users/RCOLL/Downloads/chromedriver_win32/chromedriver.exe')
    driver.delete_all_cookies()
    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    driver.quit()
    # Extracción de la información del HTML obtenido en el paso anterior
    nombre = soup.find_all('h1', {'class': 'c-ranking-header__title'})[0].get_text()
    ranking_actual = soup.find_all('p', {'class': 'c-ranking-header__data'})[0].get_text()
    puntos = soup.find_all('p', {'class': 'c-ranking-header__data'})[1].get_text()
    p_jugados = soup.find_all('p', {'class': 'c-ranking-header__data'})[2].get_text()
    p_ganados = soup.find_all('p', {'class': 'c-ranking-header__data'})[3].get_text()
    p_perdidos = soup.find_all('p', {'class': 'c-ranking-header__data'})[4].get_text()
    efectividad = soup.find_all('p', {'class': 'c-ranking-header__data'})[5].get_text()
    vict_consecutivas = soup.find_all('p', {'class': 'c-ranking-header__data'})[6].get_text()
    link = url # Cambiar el 0 por el índice cuando creeemos el loop
    # Insertamos la info en el diccionario
    player_dict['nombre'].append(nombre)
    player_dict['ranking_actual'].append(ranking_actual)
    player_dict['puntos_wpt'].append(puntos)
    player_dict['p_jugados'].append(p_jugados)
    player_dict['p_ganados'].append(p_ganados)
    player_dict['p_perdidos'].append(p_perdidos)
    player_dict['efectividad'].append(efectividad)
    player_dict['vict_consecutivas'].append(vict_consecutivas)
    player_dict['url'].append(link)
    # Añadimos cierta variabilidad en la ejecución para evitar que nos bloqueen
    seg = random.randrange(1, 4, 1)
    time.sleep(seg)

print(player_dict)

# Creación lista con el resto de URLs no recorridas
len(urls)
len(scanned_urls)

# -------------------------------
# Creación de un df con la información extraída
# -------------------------------

# Diccionario a pandas df
df = pd.DataFrame(player_dict)
df.head(5)

# -------------------------------
# Generamos el fichero .csv con el dataset
# -------------------------------

df.to_csv('C:/Users/RCOLL/Downloads/wpt_ranking_masculino.csv')
# df.to_csv('C:/Users/RCOLL/Downloads/wpt_ranking_femenino.csv') # ranking femenino

