import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

"""
The first thing we’ll need to do to scrape a web page is to download the page. We can download pages using the Python requests library.
The requests library will make a GET request to a web server, which will download the HTML contents of a given web page for us.
"""

import requests
page = requests.get('https://oxylabs.io/blog')
page.status_code # 200 = ok
print(page.status_code)
page.content

"""
We can use the BeautifulSoup library to parse this document, and extract the text from the p tag. 
"""

soup = BeautifulSoup(page.content,'html.parser')
print(soup.prettify())
list(soup.children)

test = soup.find_all("a")
# print(test)

for link in test:
    if "United" in link.text:
        print(link)
        print(link.attrs['href'])


"""
driver = webdriver.Chrome(executable_path='C:/Users/RCOLL/Downloads/chromedriver_win32/chromedriver.exe')
driver.get('https://oxylabs.io/blog')
content = driver.page_source
soup = BeautifulSoup(content)
driver.quit() # Force browser to quit when we have the data

results = []
for element in soup.findAll(attrs='blog-card__content-wrapper'):
    title = element.find('h2')

for element in soup.findAll(attrs='blog-card__user-info__wrapper'):
    author = element.find('p')
print(author)



df = pd.DataFrame({'Names': results})

print(df)
"""