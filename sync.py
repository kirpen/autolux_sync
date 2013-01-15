# Requirments: lxml(http://pypi.python.org/pypi/lxml), pyquery(http://pypi.python.org/pypi/pyquery)
# coding=utf-8

import sqlite3
from pyquery import PyQuery as pq

search_url = 'http://www.autolux.ua/Predstavitelstva/query/filter/city'
    
def getDepartments():
    d = pq(url=search_url)
    depList = {}
    city = 'none'
    result = []
    for tr in d('tbody tr'):
        tds = d(tr).find('td')
        if len(tds) == 1:
            city = d(tds).eq(0).text()
        elif len(tds) >= 4:
            result.append(dict(city=city, department=d(tds).eq(1).text()))
    return result

conn = sqlite3.connect('autolux.sqlite3')
c = conn.cursor()
c.execute('''CREATE TABLE departments
             (id INTEGER PRIMARY KEY, city TEXT, department TEXT)''')
conn.commit()


for dep in getDepartments():
    c.execute("INSERT INTO departments (city, department) VALUES ('" + dep['city'] + "', '" + dep['department'] + "')")


conn.commit()
conn.close()
print('Compleated')
