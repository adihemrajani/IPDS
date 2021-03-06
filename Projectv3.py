#Question 1
# need to install pandas through -> easy_install pandas

from bs4 import BeautifulSoup
import pandas as pd
import requests
import csv

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
    year.append(parsed_table_data[i][6][0:4])

def CleanRatio(raw_ratio):
    s = raw_ratio.split("%")
    return float(s[0])/100.00

clean_ratios = []
for ratio in ratios:
    clean_ratios.append(CleanRatio(ratio))

def CleanFareSystem(fs):
    cfs = fs.strip().lower()
    return cfs

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

for farerate_unit in farerate:
    if 'US$' in farerate_unit[0:3]:
        segment = farerate_unit.split('US$')[1][0:4].strip()
        if '+' in segment:
            segment = segment.split('+')[0].strip()
        if '-' in segment:
            segment = segment.split('-')[0].strip()
        if '(' in segment:
            segment = segment.split('(')[0].strip()
        if ' ' in segment:
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
    if 'EUR' in farerate_unit[0:3]:
        if '-' in farerate_unit:
            clean_farerate.append(float(farerate_unit.split('EUR')[1].split('-')[0].strip()) * eur_converter)
        elif '+' in farerate_unit:
            clean_farerate.append(float(farerate_unit.split('EUR')[1].split('+')[0].strip()) * eur_converter)
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
    clean_year.append(year_unit)

bycolumns_cleaned = []
bycolumns_cleaned.append(parsed_table_data[0])
bycolumns_cleaned.append(parsed_table_data[1])
bycolumns_cleaned.append(parsed_table_data[2])
bycolumns_cleaned.append(clean_ratios)
bycolumns_cleaned.append(clean_faresystem)
bycolumns_cleaned.append(clean_farerate)
bycolumns_cleaned.append(clean_year)

for i in clean_farerate:
    print(i)

#with open('Farebox_Recovery_Ratio_Analysis.csv', mode = 'wb') as faredata_file:
#    faredata_writer = csv.writer(exam_responses_file)
#    faredata_writer.writerow(headers)
#    for  in :
#        responses = exam_responses[student_name]
#        exam_writer.writerow([student_name] + [responses[question] for question in question_keys])


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
