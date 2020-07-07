from flask import Flask, jsonify
import pymongo
import os

app = Flask(__name__)

def connect_to_database():
    MONGODB_URI = os.environ['MONGODB_URI']
    client = pymongo.MongoClient(MONGODB_URI,retryWrites = False)
    db = client['heroku_672rlh8s']
    collection_name = 'covid_stats'
    collection = db[collection_name]
    return collection


@app.route('/getData')
def main():
    collection = connect_to_database()
    query = {}
    projection = {"_id": 0}

    cursor = collection.find(query,projection)
    data = [i for i in cursor]
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
