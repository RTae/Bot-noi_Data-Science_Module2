#coding=utf-8

import bs4
import requests
import pymongo
import os
from selenium import webdriver
import urllib.request
import datetime
import re

def connect_database(collection_name):
    '''
    Use to connect to nosql database (MongoDB)
    arg : None
    return : collection 
    '''
    MONGODB_URI = os.environ['MONGODB_URI']
    client = pymongo.MongoClient(MONGODB_URI,retryWrites = False)
    dbName = MONGODB_URI.split(':')[1][2:]
    db = client[dbName]
    if collection_name not in db.list_collection_names():
        db.create_collection(collection_name)
    collection = db[collection_name]

    return collection

def scrape_all_document(category):
    '''
    Scrape data from Thairath News in Category of foreign
    arg : None
    return : Document [Dict]
    '''
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(
        executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options
    )
    url = os.environ.get('URL')+category
    print(url)
    driver.get(url)
    res = driver.execute_script('return document.documentElement.outerHTML')
    driver.quit()

    page = bs4.BeautifulSoup(res, 'html.parser')
    response = page.find('aside',{'class':'css-1xuuifk eqom6ue5'})
    selector = 'div.container > div.row > div.col-md-3'
    response = response.select(selector)

    Document = []

    for data in response:
        news = data.select('div.css-1ugzggj.e9fvmtc0 a')
        link = news[0]['href']
        link = url[:26]+str(link)
        data = scrape_document(link)
        Document.append(data)

    return Document

def scrape_document(news_url):
    '''
    Scrape data from Thairath News from each news
    arg : news_url
    return : {
            'title : Name of the news [String]'
            'publish_date' : Date time of the news[Datetime object],
            'desc' : Description of the news [String],
            'tags' : The tag that connected to the news [Array],
            'cover_img' : Picture of that news [String],
            'news_url' : Link of the news [String],
            'category' : Category of the news [String],
            } [Dict]
    '''
    res = requests.get(news_url).content
    page = bs4.BeautifulSoup(res, 'html.parser')

    selector = 'div.css-1qqrjyc.evs3ejl0 > article#article-content > div > h1'
    title = page.select(selector)[0].text

    selector = 'div.css-1qqrjyc.evs3ejl0 > article#article-content > div.css-og303v.evs3ejl10 > div.css-1cxbv8p.evs3ejl7 > span.css-x2q8w.e1ui9xgn2'
    publish_date = page.select(selector)[0].text
    publish_date = convert_string_to_objectTime(publish_date)

    selector = 'div.css-1qqrjyc.evs3ejl0 > article#article-content > div.css-n5piny.evs3ejl1 div'
    list_sentence = [div.text for div in page.select(selector)]
    sentence = ''
    for text in list_sentence:
        sentence+=text.strip().replace('\n','')
    desc = sentence

    selector = 'div.css-1qqrjyc.evs3ejl0 > div.css-sq8bxp.evs3ejl16 > span > a'
    tags = [ tag.text for tag in page.select(selector) ]

    selector = 'div.css-1qqrjyc.evs3ejl0 > article#article-content > div.css-1w5ifek.evs3ejl11 > picture > img'
    cover_img = page.select(selector)[0]['src']

    selector = 'div.css-1qqrjyc.evs3ejl0 > article#article-content > div.css-og303v.evs3ejl10 > div.css-7enauw.evs3ejl43 > a'
    category = page.select(selector)[1].text
    
    return {
            'title' : title,
            'publish_date' : publish_date,
            'desc' : desc,
            'tags' : tags,
            'cover_img' : cover_img,
            'news_url' : news_url,
            'category' : category,
            }

def convert_string_to_objectTime(timesString):
    '''
    convert time that come from string format to obect time format
    arg : timesString [String]
    return : time [Datetime object]
    '''
    thai_abbr_months = {
                "ม.ค.":'1',
                "ก.พ.":'2',
                "มี.ค.":'3',
                "เม.ย.":'4',
                "พ.ค.":'5',
                "มิ.ย.":'6',
                "ก.ค.":'7',
                "ส.ค.":'8',
                "ก.ย.":'9',
                "ต.ค.":'10',
                "พ.ย.":'11',
                "ธ.ค.":'12',
                }
    time = timesString.replace('น.','')
    time = time.split()
    time[1] = thai_abbr_months[time[1]]
    time = str(int(time[2])-543)+'-'+time[1]+'-'+time[0]+' '+time[3]
    time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M')
    return time

def insert_document(collection,document):
    '''
    Insert document to specific collection
    arg : collection,
          document [Dict]
    return : None
    '''
    title_list , state = checkSameNews_query_document(collection,document)
    if state:
        document_title_list = [doc['title'] for doc in document]
        for title in title_list:
            index =  document_title_list.index(title)
            document.pop(index)
            document_title_list.pop(index)
        if len(document) != 0:
            collection.insert_many(document)
    else:
        collection.insert_many(document)
    
    print('Insert Done !!')
    
def checkSameNews_query_document(collection,document):
    '''
    check the news exist on the database
    arg : collection,
          document [Dict]
    return : [list],[bool]
    '''
    document_title = [doc['title'] for doc in document]
    query = { "title": {"$in": document_title} }
    cursor = collection.find(query)
    if (cursor.count() == 0):
        return [],False
    else:
        oldNews_title = [doc['title'] for doc in cursor]
        return oldNews_title,True


def main():
    collection_category = [
        'thairathNews_foreign',
        'thairathNews_business',
        'thairathNews_local',
        'thairathNews_royal',
        'thairathNews_society',
        'thairathNews_crime',
    ]

    for cat in collection_category:
        print(cat)
        collection = connect_database(cat)
        document = scrape_all_document(cat.split('_')[1])
        insert_document(collection,document)

main()