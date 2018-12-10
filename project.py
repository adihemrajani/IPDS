#Question 1
#on terminal: python -m pip install pandas
# need to install pandas through -> easy_install pandas
import pandas
from pandas.io.html import read_html
import pickle
import sqlite3

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
fare system = table[4]
fare rate = table[5]
year = table[6]

#Question 2
def CleanRatio(raw_ratio):
    s = raw_ratio.split("%")
    return float(s[0])/100.00

clean_ratio = []
for rate in ratio:
    #print(CleanRate(rate))
    clean_ratio.append(CleanRate(rate))

#Question 3 code that creates the table (we are going to have transit, with the rate, contintent etc)
create_table_sql = """ CREATE TABLE IF NOT EXISTS ratios (
                                        rate REAL
                                        country TEXT,
                                        continent TEXT,
                                        ) ; """
cur = conn.cursor()
cur.execute(create_table_sql)

#for rate, country, continent in zip
for rate in clean_rates:
    sql = """ INSTERT INTO rates VALUES (%s, %s, %s, %s); """ % rate
    print(sql)
    cur.execute(sql)
    conn.commit()
