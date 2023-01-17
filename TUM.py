# This is a sample Python script.

import requests
import lxml
from bs4 import BeautifulSoup
import re
import csv
import pandas as pd
from collections import defaultdict

# Part 1 – Get the HTML using Requests

url = 'https://www.bio.nat.tum.de/biotech/forschungsgruppe/aktuelle-mitarbeiter/'
response = requests.get(url)
# Check the connection to ensure that the website returned content rather than an error:
# print(response.status_code)

# Part 2 – Find the element
soup = BeautifulSoup(response.text, 'lxml')  # lxml parser
results = soup.find_all('div', {'class': 'ce-bodytext'})
Faculty_Name = []
records = []

for result in results:
    mail = re.sub(r"mailto:", "", result.find('a').attrs['href'])
    faculty_name = result.find_all("h4", {"class": "hx"})
    # Find font style class text value
    # font_style_class_values = soup.find_all("h4", {"class": "hx"})
    for font_style_class_value in faculty_name:
        Faculty_Name = font_style_class_value.text
    records.append(Faculty_Name)
records = [s.replace('\n', '').replace('\t', '') for s in records]

faculty_name = {}
fac_data = []
for fn in records:
    fac_data.append({'key': 'faculty_name', 'value': fn})

list1 =[]
for i in soup.find_all('tr'):
    list1.append(i.text)

data = []
counter = 0

for s in list1:
    if ':' in s:
        parts = s.split(':')
        if len(parts) >= 2:
            key, value = s.rsplit(':', 1)
            if key.strip() =='Mail' or key.strip() == 'Raum' or key.strip() == 'Telefon':
                counter = counter + 1
                data.append({'key': key.strip(), 'value': value.strip()})

for element in fac_data:
    data.append(element)
people = {}

# Iterate through the data and store it in the dictionary
for row in data:
    key = row['key']
    value = row['value']
    if key in ['Mail', 'Raum', 'Telefon', 'faculty_name']:
        people.setdefault(key, []).append(value)

# Flatten the dictionary into a list of rows
rows = [[k, *v] for k, v in people.items()]

# Transpose the rows to get the columns
columns = list(map(list, zip(*rows)))

# Write the columns to the CSV file
with open('TUM.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(columns)



