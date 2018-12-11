#Question 1
# need to install pandas through -> easy_install pandas

from bs4 import BeautifulSoup
import pandas as pd
import requests

website = requests.get("https://en.wikipedia.org/wiki/Farebox_recovery_ratio")
soup = BeautifulSoup(website.content,'lxml')
tabularform = soup.find_all('table', {'class':'sortable'})
features = 'html parser'
newtable = pd.DataFrame()
parsed_table_data = []

rows = tabularform[0].find_all("tr")
for row in rows:
    children = row.findChildren(recursive = False)
    rowtext = []
    for child in children:
        cleantext = child.text # This is to discard reference/citation links
        cleantext = cleantext.split('&#91;')[0] # This is to clean the header row of the sort icons
        cleantext = cleantext.split('&#160;')[-1]
        cleantext = cleantext.strip()
        rowtext.append(cleantext)
    parsed_table_data.append(rowtext)

headers = parsed_table_data[0]
continent = []
country = []
systemname = []
ratios = []
faresystem = []
farerate = []
year = []

for i in range(1, len(parsed_table_data)): # Cycle through elements 1 to the end
    continent.append(parsed_table_data[i][0].strip(" ")) # Excluding trailing or leading spaces
    country.append(parsed_table_data[i][1].strip(" ")) # Excluding trailing or leading spaces
    systemname.append(parsed_table_data[i][2].strip(" ")) # Excluding trailing or leading spaces
    ratios.append(parsed_table_data[i][3])
    faresystem.append(parsed_table_data[i][4])
    farerate.append(parsed_table_data[i][5])
    year.append(parsed_table_data[i][6])

def CleanRatio(raw_ratio):
    s = raw_ratio.split("%")
    return float(s[0])/100.00

clean_ratios = []
for ratio in ratios:
    clean_ratios.append(CleanRatio(ratio))

for i in parsed_table_data:
    print(i)

'''
alldata = pd.DataFrame(columns =['Continent', 'Country', 'System', 'Ratio', 'Fare system', 'Fare rate', 'Year'] )

    df2 = pd.DataFrame(i)
    alldata.append(df2)

print(alldata)


master = {} # Dictionary containing data by attribute - Adi

keys = []
for header in parsed_table_data[0]: # Cycle through headers in element 0
    keys.append(header)

print(keys)

values = []
for i in range(1,len(parsed_table_data)): # Cycle through elements 1 to the end
    for j in range(1, len(parsed_table_data[i])): # Cycle through elements 1 to 7 in
        for value in : # Within each element
        values()
# print(row.text)

'''
'''
df = pd.read_html(str(table))[0]
countries = df["COUNTRY"].tolist()
users = df["AMOUNT"].tolist()
'''
'''
from pandas.io.html import read_html
import pickle

#load sqlite3 package
db_file = "rates.db"
conn = sqlite3.connect(db_file)

refresh = False

if refresh:
    page = "https://en.wikipedia.org/wiki/Farebox_recovery_ratio"
    wikitables = read_html(page)
    table = wikitables[1]
    pickle.dump(table, open("wiki_table.pkl", "w"))
else:
    table = pickle.load(open("wiki_table.pkl", "r"))

continent = table[0]
country = table[1]
system = table[2]
ratio = table[3][1:]
faresystem = table[4]
farerate = table[5]
year = table[6]

def CleanRatio(raw_ratio):
    s = raw_ratio.split("%")
    return float(s[0]/100.00)

clean_ratios = []
for ratio in ratios:
    #print(CleanRate(rate))
    clean_rates.append(CleanRate(ratios))
'''
