from bs4 import BeautifulSoup
import requests

page = requests.get('https://www.fs.usda.gov/detailfull/mthood/alerts-notices/?cid=stelprdb5191108&width=full')

if(page.status_code == 200):
    soup = BeautifulSoup(page.content, 'lxml')
    #print(soup.prettify())
    all_tables = soup.find_all('table')
    data = []
    for table in all_tables:

        table_body = table.find('tbody')
        header_check = table_body.find("tr").find("td").text.strip()

        if(header_check == 'Road Number'):  #make sure it is a table with road info in it
            rows = table_body.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                if cols:
                    data.append([ele for ele in cols if ele])  # Get rid of empty values

    for row in data:
        #print(row)
        if row[0] == "3512":
            print(row)
            break

from google.cloud import firestore

# The `project` parameter is optional and represents which project the client
# will act on behalf of. If not supplied, the client falls back to the default
# project inferred from the environment.
db = firestore.Client(project='fs-road-status')

roads_ref = db.collection(u'roads')
docs = roads_ref.stream()

for doc in docs:
    print(f'{doc.id} => {doc.to_dict()}')