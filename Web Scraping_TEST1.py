import requests
from bs4 import BeautifulSoup


def scrape_page(page_url):
    """Extracts HTML from a webpage"""

    answer = requests.get(page_url)
    content = answer.content
    soup = BeautifulSoup(content, features='html.parser')

    return soup

print(scrape_page("https://www.hometogo.com/"))