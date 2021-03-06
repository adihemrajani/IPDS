#Question 1
from bs4 import BeautifulSoup # Need to import beautiful soup to pull data out of HTML and XML files
import pandas as pd # Need to import pandas to take data to create a python object with rows and columns called a data frame
import requests # Need to import requests to handle HTTP related operation
import csv # Need to import csv to read and write tabular data in CSV format
import sqlite3 # Need to import sqlite3 to access the database using a variant of the sql language

conn = sqlite3.connect("FareboxRecoveryRatioAnalysis.sqlite") # To use the module, we must first create a connection object that represents the database. Here, the data is stored in the FareBoxRecoverRatioAnalysis file.
cur = conn.cursor() # Once we have the connection, we create a cursor object 

website = requests.get("https://en.wikipedia.org/wiki/Farebox_recovery_ratio") # Pull data from this link 
soup = BeautifulSoup(website.content,'lxml') #'lxml' allows us to parse XML and HTML documents
tabularform = soup.find_all('table', {'class':'sortable'}) # Find the table on the Wikipedia page
features = 'html parser'
newtable = pd.DataFrame() # Two dimensional tabular data structure with rows and columns
parsed_table_data = [] # Create an open list called parsed_data_table

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
# Create a for loop that appends the open list, parsed_data_table, with the clean text

headers = ['Continent', 'Country', 'System', 'Ratio', 'Fare System', 'Fare Rate (US$)', 'Year']
continent = []
country = []
systemname = []
ratios = []
faresystem = []
farerate = []
year = []
# Create open lists for all headers in the table 

for i in range(1, len(parsed_table_data)): # Cycle through elements 1 to the end
    continent.append(parsed_table_data[i][0].strip(" ")) # Excluding trailing or leading spaces
    country.append(parsed_table_data[i][1].strip(" ")) # Excluding trailing or leading spaces
    systemname.append(parsed_table_data[i][2].strip(" ")) # Excluding trailing or leading spaces
    ratios.append(parsed_table_data[i][3]) # Pulling the 4th column of the Wikipedia table
    faresystem.append(parsed_table_data[i][4]) # Pulling the 5th column of the Wikipedia table
    farerate.append(parsed_table_data[i][5]) # Pulling the 6th column of the Wikipedia table
    year.append(parsed_table_data[i][6][0:4]) # Pulling the year from the 7th column of the Wikipedia table, excluding the superscipt

def CleanRatio(raw_ratio):
    s = raw_ratio.split("%")
    return float(s[0])/100.00
# Define a function called CleanRatio that excludes the "%" sign and converts the ratio into a float

clean_ratios = []
for ratio in ratios:
    clean_ratios.append(CleanRatio(ratio))
# Create a for loop that appends the list, clean_ratios, using the function CleanRatio

def CleanFareSystem(fs):
    cfs = fs.strip().lower()
    return cfs
# Define a function called CleanFareSystem that converts words to lowercase

clean_faresystem = []
for faresystem_unit in faresystem:
    if "flat rate" in CleanFareSystem(faresystem_unit):
        faresystem_unit = "flat rate"
        clean_faresystem.append(CleanFareSystem(faresystem_unit))
    elif "zone based" in CleanFareSystem(faresystem_unit):
        faresystem_unit = "zone based"
        clean_faresystem.append(CleanFareSystem(faresystem_unit))
    else:
        clean_faresystem.append(CleanFareSystem(faresystem_unit))
# Create a for loop that appends the list, clean_faresystem, using the function CleanFareSystem which will standardize all of the "flat rate" and zone based" terms

# Conversion Rates to USD i.e. Quantity of USD Comprising Each Currency
clean_farerate = []
eur_converter = 1.13
hkd_converter = 0.13
czk_converter = 0.044
chf_converter = 1
cad_converter = 0.75
aus_converter = 0.72
gbp_converter = 1.26
sek_converter = 0.11
jpy_converter = 0.0088
pkr_converter = 0.0072
nt_converter = 0.032
cny_converter = 0.14
sgd_converter = 0.73

# Clean the Fare rate column 
for farerate_unit in farerate: 
    if 'US$' in farerate_unit[0:3]: 
        segment = farerate_unit.split('US$')[1][0:4].strip() 
        if '+' in segment:
            segment = segment.split('+')[0].strip()
        elif '-' in segment:
            segment = segment.split('-')[0].strip()
        elif '(' in segment:
            segment = segment.split('(')[0].strip()
        elif ' ' in segment:
            segment = segment.split(' ')[0].strip()
        #    clean_farerate.append(float(segment.split(' ')[0].strip()))
        #    clean_farerate.append(float(segment.split('-')[0].strip()))
        #if '-' in segment:
            #clean_farerate.append(float(segment.split('-')[0].strip()))
        #    segment.split('-')[1].strip()
    #    if '1.25' in segment:
    #        clean_farerate.append(1.25)
    #    if '+' in segment:
    #        segment.split('+')[0].strip()
    #    if '(' in segment:
    #        #clean_farerate.append(float(segment.split('(')[0].strip()))
    #        segment.split('(')[0].strip()
    #    if '/' in segment:
    #        #clean_farerate.append(float(farerate_unit.split('US$')[1].split('/')[0].strip()))
    #        segment.split('/')[0].strip()
    #    if ',' in segment:
            #clean_farerate.append(float(farerate_unit.split('US$')[1].split(',')[0].strip()))
    #        segment.split(',')[0].strip()
        clean_farerate.append(float(segment))
    elif 'EUR' in farerate_unit[0:3]:
        if '-' in farerate_unit:
            clean_farerate.append(float(farerate_unit.split('EUR')[1].split('-')[0].strip()) * eur_converter)
        elif '+' in farerate_unit:
            clean_farerate.append(float(farerate_unit.split('EUR')[1].split('+')[0].strip()) * eur_converter)
        else:
            clean_farerate.append(float(farerate_unit.split('EUR')[1].strip()) * eur_converter)
    elif 'HK$' in farerate_unit[0:3]:
        clean_farerate.append(float(farerate_unit.split('HK$')[1].split('+')[0].strip()) * hkd_converter)
    elif 'CZK' in farerate_unit[0:3]:
        clean_farerate.append(float(farerate_unit.split('CZK')[1].split('+')[0].strip()) * czk_converter)
    elif 'CHF' in farerate_unit[0:3]:
        clean_farerate.append(float(farerate_unit.split('CHF')[1].split('+')[0].strip()) * chf_converter)
    elif 'C$' in farerate_unit[0:3]:
        clean_farerate.append(float(farerate_unit.split('C$')[1].split(' ')[0].split('+')[0].strip()) * cad_converter)
    elif 'A$' in farerate_unit[0:3]:
        segment = farerate_unit.split('A$')[1]
        if '/' in segment:
            clean_farerate.append(0.15)
        else:
            clean_farerate.append(float(segment))
    elif 'From' in farerate_unit[0:4]:
            clean_farerate.append(3.76)
    elif '€' in farerate_unit[0:3]:
        clean_farerate.append(float(farerate_unit.split('€')[1].split('+')[0].strip()) * gbp_converter)
    elif 'SEK' in farerate_unit[0:3]:
        clean_farerate.append(float(farerate_unit.split('SEK')[1].split('-')[0].strip()) * sek_converter)
    elif '¥' in farerate_unit[0:3]:
        clean_farerate.append(float(farerate_unit.split('¥')[1].split('+')[0].strip()) * jpy_converter)
    elif 'PKR' in farerate_unit[0:3]:
        clean_farerate.append(float(farerate_unit.split('PKR')[1].split('+')[0].strip()) * pkr_converter)
    elif 'NT$' in farerate_unit[0:3]:
        clean_farerate.append(float(farerate_unit.split('NT$')[1].split('+')[0].strip()) * nt_converter)
    elif 'CNY' in farerate_unit[0:3]:
        clean_farerate.append(float(farerate_unit.split('CNY')[1].split('+')[0].strip()) * cny_converter)
    elif 'SGD' in farerate_unit[0:3]:
        clean_farerate.append(float(farerate_unit.split('SGD')[1].split('+')[0].strip()) * sgd_converter)
    else:
        clean_farerate.append('n/a')

clean_year = []

for year_unit in year:
    clean_year.append(int(year_unit))

bycolumns_cleaned = []
bycolumns_cleaned.append(continent)
bycolumns_cleaned.append(country)
bycolumns_cleaned.append(systemname)
bycolumns_cleaned.append(clean_ratios)
bycolumns_cleaned.append(clean_faresystem)
bycolumns_cleaned.append(clean_farerate)
bycolumns_cleaned.append(clean_year)

byrows_cleaned = []
eachrow = []
'''for i in range(0, len(bycolumns_cleaned)):
    for j in range(0, len(bycolumns_cleaned[0])):
        byrows_cleaned.append(continent[i][j]) '''

for each_system in range(0, len(bycolumns_cleaned[0])):
    newrow = []
    newrow.append(continent[each_system])
    newrow.append(country[each_system])
    newrow.append(systemname[each_system])
    newrow.append(clean_ratios[each_system])
    newrow.append(clean_faresystem[each_system])
    newrow.append(clean_farerate[each_system])
    newrow.append(clean_year[each_system])
    byrows_cleaned.append(newrow)

with open('Farebox_Recovery_Ratio_Analysis.csv', mode = 'w') as faredata_file: # Open the Farebox_Recovery_Ratio_Analysis file, and set mode to 'w' to edit and write new information to the file
    faredata_writer = csv.writer(faredata_file) 
    faredata_writer.writerow(headers) 
    for i in range(0, len(byrows_cleaned)):
        faredata_writer.writerow(byrows_cleaned[i])

create_table_sql = """CREATE TABLE IF NOT EXISTS FareboxDataAnalysis (
                                        continent TEXT,
                                        country TEXT,
                                        system TEXT,
                                        ratio FLOAT,
                                        faresystem TEXT,
                                        farerate FLOAT,
                                        year INTEGER);"""

cur.execute(create_table_sql)

for i in range(0, len(byrows_cleaned)):
    continent = byrows_cleaned[i][0]
    country = byrows_cleaned[i][1]
    faresystem = byrows_cleaned[i][2]
    fr = byrows_cleaned[i][3]
    fs = byrows_cleaned[i][4]
    rate = byrows_cleaned[i][5]
    year = str(byrows_cleaned[i][6])
    sql = """INSERT OR REPLACE INTO FareboxDataAnalysis VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s");""" % (continent, country, faresystem, fr, fs, rate, year)
    cur.execute(sql)
    conn.commit()

'''
alldata = pd.DataFrame(columns =['Continent', 'Country', 'System', 'Ratio', 'Fare system', 'Fare rate', 'Year'] )

    df2 = pd.DataFrame(i)
    alldata.append(df2)

print(alldata)

'''

'''
df = pd.read_html(str(table))[0]
countries = df["COUNTRY"].tolist()
users = df["AMOUNT"].tolist()

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

'''
