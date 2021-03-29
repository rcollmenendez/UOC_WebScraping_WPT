"""
@author:

"""

"""
    Configurando el entorno
"""
import time
from selenium import webdriver
from bs4 import BeautifulSoup

"""
    Inicio
"""

# Web scrapper for infinite scrolling page
driver = webdriver.Chrome(executable_path='C:/Users/RCOLL/Downloads/chromedriver_win32/chromedriver.exe')
driver.get("https://www.worldpadeltour.com/jugadores?ranking=todos")
time.sleep(2)  # Allow 2 seconds for the web page to open
scroll_pause_time = 2 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
i = 1

while True:
    # scroll one screen height each time
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
    i += 1
    time.sleep(scroll_pause_time)
    # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
    scroll_height = driver.execute_script("return document.body.scrollHeight;")  
    # Break the loop when the height we need to scroll to is larger than the total scroll height
    if (screen_height) * i > scroll_height:
        break


##### Extract Reddit URLs #####
urls = []
soup = BeautifulSoup(driver.page_source, "html.parser")

for element in soup.find_all("li", {"class": "c-player-card__item"}):
    name = element.find("a", {"class": "c-trigger"})['href']
    urls.append(name)

for x in urls:
   print(x)

"""
Información Jugador
"""

urls[0]


driver = webdriver.Chrome(executable_path='C:/Users/RCOLL/Downloads/chromedriver_win32/chromedriver.exe')
# Abrimos la página con Chrome
driver.delete_all_cookies()
driver.get('https://www.worldpadeltour.com/jugadores/alejandro-galan-romo')
content = driver.page_source
soup = BeautifulSoup(content,'html.parser')
driver.quit() # Force browser to quit when we have the data


ranking = soup.find_all('p',{'class': 'c-ranking-header__data'})[0]



