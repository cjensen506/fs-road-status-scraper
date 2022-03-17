from bs4 import BeautifulSoup
import requests
from google.cloud import firestore
from google.cloud import secretmanager

def hello_pubsub(event, context):

    # Scrape the webpage
    page = requests.get('https://www.fs.usda.gov/detailfull/mthood/alerts-notices/?cid=stelprdb5191108&width=full')

    if (page.status_code == 200):
        soup = BeautifulSoup(page.content, 'lxml')
        all_tables = soup.find_all('table')
        data = []
        for table in all_tables:

            table_body = table.find('tbody')
            header_check = table_body.find("tr").find("td").text.strip()

            if (header_check == 'Road Number'):  # make sure it is a table with road info in it
                rows = table_body.find_all('tr')
                for row in rows:
                    cols = row.find_all('td')
                    cols = [ele.text.strip() for ele in cols]
                    if cols:
                        data.append([ele for ele in cols])  # Get rid of empty values

    #pull from database roads of interest
    db = firestore.Client(project='fs-road-status')

    roads_ref = db.collection(u'roads')
    docs = roads_ref.stream()

    roads_of_interest = []
    for doc in docs:
        road_of_interest_dict = doc.to_dict()
        for row in data:
            if (row[0] == road_of_interest_dict['road_number']) & (row[1] == road_of_interest_dict['road_name']):
                if (row[2] != road_of_interest_dict['status']) | (row[3] != road_of_interest_dict['conditions_updates']):
                    # change in road status
                    # update the database
                    doc.reference.update({u'status': row[2]})
                    doc.reference.update({u'conditions_updates': row[3]})

                    # send webhook alert
                    client = secretmanager.SecretManagerServiceClient()
                    name = f"projects/361740823008/secrets/webhook_url/versions/1"

                    # Access the secret version.
                    response = client.access_secret_version(request={"name": name})
                    webhook_url = response.payload.data.decode("UTF-8")

                    myobj = {'text': ' '.join([str(elem) for elem in row])}
                    x = requests.post(webhook_url, json=myobj)


if __name__ == "__main__":
   hello_pubsub(event="", context="")
