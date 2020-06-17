from flask import Flask, jsonify, request
import requests
import json
import pandas as pd

main = Flask(__name__)

@main.route('/hello')
def index():
    return 'Hello'

@main.route('/hello1')
def index1():
    return 'Hello1'

@main.route('/hello2')
def index2():
    return 'Hello2'

@main.route('/data')
def data():
    return jsonify(
        {'Name' : 'Tae',},
        {'Name':'Jo'})

@main.route('/profile/dict')
def myname():
    return {
        'Name' : 'Tae',
        'Age' : 21,
        'Education': 'KMUTT'
    }

# accept input parameters
@main.route('/param')
def get_parameters():
    param1 = request.args.get('param1')
    param2 = request.args.get('param2')
    param3 = request.args.get('param3')
    try:
        param3 = int(param3)
    except:
        return 'Give me a numbers'
        
    return {
        'Param1' : param1,
        'Param2' : param2,
        'Param3' : param3
    }

@main.route('/add')
def addMedthod():
    num1 = request.args.get('num1',type=float)
    num2 = request.args.get('num2',type=float)

    return {'Result':num1+num2}

@main.route('/muti')
def mutiMedthod():
    num1 = request.args.get('num1',type=float)
    num2 = request.args.get('num2',type=float)

    return {'Result':num1*num2}

@main.route('/div')
def divMedthod():
    num1 = request.args.get('num1',type=float)
    num2 = request.args.get('num2',type=float)

    return {'Result':num1/num2}

@main.route('/covid')
def covid():
    response = requests.get('https://covid19.th-stat.com/api/open/timeline')
    data = response.json()['Data']
    Date = request.args.get('date',type=str)
    NewConfirmed = request.args.get('newconfirmed',type=int)
    NewRecovered = request.args.get('newrecovered',type=int)
    NewHospitalized = request.args.get('newhospitalized',type=int)
    NewDeaths = request.args.get('newdeaths',type=int)
    Confirmed = request.args.get('recovered',type=int)
    Recovered = request.args.get('confirmed',type=int)
    Hospitalized = request.args.get('hospitalized',type=int)
    Deaths = request.args.get('Deaths',type=int)

    results = Fillter(data,NewConfirmed,NewRecovered,NewHospitalized,NewDeaths,Recovered,Confirmed,Hospitalized,Deaths,Date)
    
    return (results)

def Fillter(data,NewConfirmed,NewRecovered,NewHospitalized,NewDeaths,Recovered,Confirmed,Hospitalized,Deaths,Date):

    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'],format='%m/%d/%Y')
    query = 1
    Date_Start,Date_Final = Date.split(',')
    Date_Final = pd.to_datetime(Date_Final,format='%m/%d/%Y')
    Date_Start = pd.to_datetime(Date_Start,format='%m/%d/%Y')

    if NewConfirmed is not None:
        query = query & (df['NewConfirmed']==NewConfirmed)
    if NewRecovered is not None:
        query = query & (df['NewRecovered']==NewRecovered)
    if NewHospitalized is not None:
        query = query & (df['NewHospitalized']==NewHospitalized)
    if NewDeaths is not None:
        query = query & (df['NewDeaths']==NewDeaths)
    if Recovered is not None:
        query = query & (df['Recovered']==Recovered)
    if Confirmed is not None:
        query = query & (df['Confirmed']==Confirmed)
    if Hospitalized is not None:
        query = query & (df['Hospitalized']==Hospitalized)
    if Deaths is not None:
        query = query & (df['Deaths']==Deaths)
    if Date is not None:
        query = query & ((df['Date']>=Date_Start) & (df['Date']<=Date_Final))

    df = df[query]
    result_json = json.loads(df.to_json(date_format='iso',orient='records'))

    return jsonify(result_json)

# Example : Serving covid data from file
with open('today_data.json','r') as f:
   data = json.load(f)

@main.route('/api/covid/all')
def covidFile():
    return jsonify(data)

if __name__ == '__main__':
    main.run(debug=True)

