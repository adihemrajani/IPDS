#Question 1
# need to install pandas through -> easy_install pandas

from bs4 import BeautifulSoup
import requests

website = requests.get("https://en.wikipedia.org/wiki/Farebox_recovery_ratio")
soup = BeautifulSoup(website.content,'lxml')
tabularform = soup.find_all('table', {'class':'sortable'})
features = 'html parser'

rows = tabularform[0].find_all("tr")
for row in rows:
    print(row.text)

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

refresh = FALSE

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
