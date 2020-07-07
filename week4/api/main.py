import bs4
import requests
import pymongo
import os

url = 'https://www.worldometers.info/coronavirus/'

def connect_to_database():
    MONGODB_URI = os.environ['MONGODB_URI']
    #MONGODB_URI = 'mongodb://heroku_hfh2p393:4hrpfv7kqfc7lp4sohk1oc2ras@ds127293.mlab.com:27293/heroku_hfh2p393'
    client = pymongo.MongoClient(MONGODB_URI,retryWrites = False)
    db = client['heroku_hfh2p393']
    collection_name = 'covid_stats'
    if collection_name not in db.list_collection_names():
        db.create_collection(collection_name)
    collection = db[collection_name]
    return collection

def scrape_data(url):
    response = requests.get(url)
    html_page = bs4.BeautifulSoup(response.content,'html.parser')

    selector = 'div.col-md-8 > div.content-inner > div'
    last_update = html_page.select(selector)[1].text[14:]

    selector = 'div#maincounter-wrap > div.maincounter-number > span'
    tag = html_page.select(selector)
    num_cases = int(tag[0].text.strip().replace(',',''))
    num_deaths = int(tag[1].text.strip().replace(',',''))
    num_recovered = int(tag[2].text.strip().replace(',',''))

    document = {'last_update': last_update,
                'num_cases': num_cases,
                'num_deaths': num_deaths,
                'num_recovered': num_recovered,
                }

    return document

def insert_to_database(collection,document):
    collection.insert_one(document)
    print(document)
    print('Document insert')

def main():
    collection = connect_to_database()
    document = scrape_data(url)
    insert_to_database(collection,document)

main()