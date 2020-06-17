import requests
import json
import pandas as pd

response = requests.get('https://covid19.th-stat.com/api/open/timeline')
data = response.json()
print(data['Data'])

with open('today_data.json','w') as f:
    f.write(json.dumps(data['Data']))