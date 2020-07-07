from flask import Flask, jsonify, render_template, request
import pymongo
import markdown
import markdown.extensions.fenced_code
from pygments.formatters import HtmlFormatter
from datetime import datetime,timedelta
import os
import random

app = Flask(__name__)

def connect_database():
    '''
    Use to connect to nosql database (MongoDB)
    arg : None
    return : collection 
    '''
    MONGODB_URI = os.environ['MONGODB_URI']
    client = pymongo.MongoClient(MONGODB_URI,retryWrites = False)
    dbName = MONGODB_URI.split(':')[1][2:]
    db = client[dbName]

    return db

def query_document(db,date,tag,limit,category):
    '''
    check the news exist on the database
    arg : db,
          date [String],
          tag [String],
          limit [int],
          category [String]

    return : [list],[bool]
    '''
    collection = db['thairathNews_'+category]
    query = {}
    if date != None and tag != None:
        date_object_start = datetime.strptime(date, '%d/%m/%Y')
        date_object_end = date_object_start + timedelta(days=1)
        query = {"$and":[{"tags": { 
                                    "$elemMatch": { 
                                                    "$eq": tag 
                                                  } 
                                  } 
                         },
                         {"publish_date": {
                                            "$gte": date_object_start, 
                                            "$lt": date_object_end
                                          } 
                         } 
                        ] 
                }
    
    elif date != None and tag == None:
        date_object_start = datetime.strptime(date, '%d/%m/%Y')
        date_object_end = date_object_start + timedelta(days=1)
        query ={"publish_date": {
                                    "$gte": date_object_start, 
                                    "$lt": date_object_end
                                } 
               }  
    
    elif date == None and tag != None:
        query = {"$and":[{"tags": { "$elemMatch": { "$eq": tag }}}]}

    projection = {"_id": 0}
    cursor = collection.find(query,projection=projection).limit(limit)
    document = [docs for docs in cursor]
    return document

def just_query_document(db,category,limit):
    '''
    Get document from collection with limit number.
    arg : db,
          category [String],
          limit [int]
    return : [list]
    '''
    projection = {"_id": 0}
    query = {}
    collection = db['thairathNews_'+category]
    cursor = collection.find(query,projection=projection).limit(limit)
    document = [docs for docs in cursor]

    return document


db = connect_database()
collection_category = [
        'foreign',
        'business',
        'local',
        'royal',
        'society',
        'crime',
    ]

@app.route('/')
def index():
    readme_file = open("readme.md", "r")
    md_template_string = markdown.markdown(
        readme_file.read(), extensions=["fenced_code"]
    )
    formatter = HtmlFormatter(style="emacs",full=True,cssclass="codehilite")
    css_string = formatter.get_style_defs()
    md_css_string = "<style>" + css_string + "</style>"
    md_template = md_css_string + md_template_string

    return md_template_string

@app.route('/getNews')
def get_news():
    date = request.args.get('date',type=str,default=None)
    tag = request.args.get('tag',type=str,default=None)
    limit = request.args.get('limit',type=int,default=1)
    category = request.args.get('category',type=str,default='foreign')

    if limit > 20 :
        limit = 20

    document = query_document(db,date,tag,limit,category)

    return jsonify(document)

@app.route('/lastestNews')
def lastest_news():

    document_list = []
    for cat in collection_category:
        document_list+=just_query_document(db,cat,5) 
    
    assert (len(document_list)) == 30 , 'Should have 30 news'

    return jsonify(document_list)

@app.route('/randomNews')
def random_news():
    cat = random.sample(collection_category,1)
    print(cat[0])
    document = just_query_document(db,cat[0],30) 
    num_rand = random.randint(0,len(document))

    return jsonify(document[num_rand])

if __name__ == '__main__':
    app.run(debug=True)