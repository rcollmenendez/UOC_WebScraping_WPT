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
import sys

# -------------------------------
# Inicio
# -------------------------------

# Cargar la página con scroll infinito
driver = webdriver.Chrome(executable_path='C:/Users/RCOLL/Downloads/chromedriver_win32/chromedriver.exe')
driver.delete_all_cookies()

# driver.get('https://www.worldpadeltour.com/jugadores?ranking=masculino') # Descargar ranking masculino
driver.get("https://www.worldpadeltour.com/jugadores?ranking=femenino") # Descargar ranking femenino

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
# Paso 1: Extracción URLs de cada jugador
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

# Fecha de actualización del ranking
reference_date = soup.find_all('div', {'class': 'c-form__group'})[0].find('p').text

# CONTROL: Comprobamos que se han cargado las URLs en la lista
if len(urls) == 0:
    sys.exit('URLs no descargadas. Revisar Paso 1')
else:
    print('Paso 1 completado. URLs descargadas')

# Limpiamos las variables que ya no vamos a necesitar
del soup

# -------------------------------
# Paso 2: Extracción información de cada jugador
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
               'companero_actual': [],
               'posicion_juego': [],
               'lugar_nacimiento': [],
               'fecha_nacimiento': [],
               'altura': [],
               'lugar_residencia': [],
               'url': [],
               'reference_date': []}

# Creamos una lista vacía para comprobar que urls se han escaneado
scanned_urls = []

# Loop para la extracción de la información de cada URL de cada jugador
for url in urls:
    scanned_urls.append(url)
    # Abrir URL de cada jugador
    driver = webdriver.Chrome(executable_path='C:/Users/RCOLL/Downloads/chromedriver_win32/chromedriver.exe')
    driver.delete_all_cookies()
    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    driver.quit()
    # Extracción de la información de rendimiento
    nombre = soup.find_all('h1', {'class': 'c-ranking-header__title'})[0].get_text()
    ranking_actual = soup.find_all('p', {'class': 'c-ranking-header__data'})[0].get_text()
    puntos = soup.find_all('p', {'class': 'c-ranking-header__data'})[1].get_text()
    p_jugados = soup.find_all('p', {'class': 'c-ranking-header__data'})[2].get_text()
    p_ganados = soup.find_all('p', {'class': 'c-ranking-header__data'})[3].get_text()
    p_perdidos = soup.find_all('p', {'class': 'c-ranking-header__data'})[4].get_text()
    efectividad = soup.find_all('p', {'class': 'c-ranking-header__data'})[5].get_text()
    vict_consecutivas = soup.find_all('p', {'class': 'c-ranking-header__data'})[6].get_text()
    link = url
    # Extracción de la información personal
    info_personal = []
    for element in soup.find_all('li', {'class': 'c-player__data-item'}):
        data = element.find('p').text
        info_personal.append(data)
    # Insertamos la info de rendimiento en el diccionario
    player_dict['nombre'].append(nombre)
    player_dict['ranking_actual'].append(ranking_actual)
    player_dict['puntos_wpt'].append(puntos)
    player_dict['p_jugados'].append(p_jugados)
    player_dict['p_ganados'].append(p_ganados)
    player_dict['p_perdidos'].append(p_perdidos)
    player_dict['efectividad'].append(efectividad)
    player_dict['vict_consecutivas'].append(vict_consecutivas)
    player_dict['url'].append(link)
    player_dict['reference_date'].append(reference_date)
    # Insertamos la info personal en el diccionario
    player_dict['companero_actual'].append(info_personal[0])
    player_dict['posicion_juego'].append(info_personal[1])
    player_dict['lugar_nacimiento'].append(info_personal[2])
    player_dict['fecha_nacimiento'].append(info_personal[3])
    player_dict['altura'].append(info_personal[4])
    player_dict['lugar_residencia'].append(info_personal[5])
    # Añadimos cierta variabilidad en la ejecución para evitar que nos bloqueen
    pausa = random.randrange(1, 4, 1)
    time.sleep(pausa)

# Creación lista con el resto de URLs no recorridas por si falla
# la descarga de información
if len(urls) > len(scanned_urls):
    urls = list(set(urls) - set(scanned_urls))

# -------------------------------
# Paso 3: Creación de un df con la información extraída
# -------------------------------

df = pd.DataFrame(player_dict)
df.head(5)

# -------------------------------
# Paso 4: Generamos el fichero .csv con el dataset
# -------------------------------

# df.to_csv('C:/Users/RCOLL/Downloads/wpt_ranking_masculino.csv')
df.to_csv('C:/Users/RCOLL/Downloads/wpt_ranking_femenino.csv') # ranking femenino
