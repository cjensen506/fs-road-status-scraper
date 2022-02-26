from bs4 import BeautifulSoup
import requests

page = requests.get('https://www.fs.usda.gov/detailfull/mthood/alerts-notices/?cid=stelprdb5191108&width=full')

if(page.status_code == 200):
    soup = BeautifulSoup(page.content, 'lxml')
    print(soup.prettify())