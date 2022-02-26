from bs4 import BeautifulSoup
import requests

page = requests.get('https://www.fs.usda.gov/detailfull/mthood/alerts-notices/?cid=stelprdb5191108&width=full')

if(page.status_code == 200):
    soup = BeautifulSoup(page.content, 'lxml')
    #print(soup.prettify())
    all_tables = soup.find_all('table')

    for table in all_tables:
        data = []
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele]) # Get rid of empty values
print(data)