import pymongo
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

url="https://saras.cbse.gov.in/SARAS/AffiliatedList/ListOfSchdirReportNew?ID1=D"
request=requests.get(url)
# print(request.text)
soup=BeautifulSoup(request.text,'html.parser')
tr=soup.find_all('tr')
# (Aff No, State & district, Status, school and head name
data={"afNo": [],"state":[],"school": [],'district':[],'status':[]}
for i in range(1,50):
    td=tr[i].find_all('td')
    data['afNo'].append(td[1].get_text())
    data['state'].append(td[2].get_text())
    data['school'].append(td[4].get_text())
    data['district'].append(td[3].get_text())
    data['status'].append(td[6].find('p').get_text())
    
df=pd.DataFrame(data)
# df.to_csv("file.csv",index=False)
d=pd.read_csv("file.csv")
print(d)


#1)
print(d.loc[d['district']=="INDORE"])

#2)
print(f"School Count: {d.count().school}")

#3)
client=pymongo.MongoClient("mongodb://localhost:27017")
db=client['school']
collection=db['n_data']

for i in range(0,10):
    state=d.iloc[i,1]
    school=d.iloc[i,2]
    district=d.iloc[i,3]
    status=d.iloc[i,4]
    collection.insert_one({"state": state,"school": school,"district":district,"status": status })
    
# 4

s=collection.find({"school": " Secondary Level"})
for i in s:
    print(i)
