import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

# Chrome driver - Importante el path
driver = webdriver.Chrome(executable_path='C:/Users/RCOLL/Downloads/chromedriver_win32/chromedriver.exe')
# Abrimos la página con Chrome
driver.delete_all_cookies()
driver.get('https://www.worldpadeltour.com/jugadores?ranking=todos')

content = driver.page_source

"""# Creamos un objeto para guardar el resultado
results = []

# Add the page source to the variable `content`.
# Load the contents of the page, its source, into BeautifulSoup
# class, which analyzes the HTML as a nested data structure and allows to select
# its elements by using various selectors.
soup = BeautifulSoup(content,"html.parser")

# Una vez tenemos los elementos en "soup" hacemos un loop
for element in soup.findAll(attrs={'class': 'c-player-card__item'}):
        name = element.find('href')
        results.append(name.text)

for x in results:
   print(x)
"""

"""
We can use the BeautifulSoup library to parse this document, and extract the text from the p tag. 
"""
soup = BeautifulSoup(content,'html.parser')

driver.quit() # Force browser to quit when we have the data

# print(soup.prettify())

forecast_items = soup.find_all(class_="c-player-card__item")

print(forecast_items)