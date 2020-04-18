import lxml.html as lh
import requests
from bs4 import BeautifulSoup
import re
# from pymongo import MongoClient

# client = MongoClient()
# db = client.get_database("stockmarket")
# posts = db.get_collection("stock")

url = "https://www.bseindia.com/markets/Equity/EQReports/mktwatchR.html?filter=Gainer*group$all$A"

page = requests.get(url)

doc = lh.fromstring(page.content)

name_list = []
req = requests.get(url)

# Initialize BeautifulSoup and parse Html Source from url above
soup = BeautifulSoup(req.content.decode('utf-8'), 'html.parser')

# Get the links for every name for 100 actors.
# Regular expressions because it proved to be useful for matching all the
# text in links that are random.

# names = soup.find("div", {"class": "col-lg-12 largetable"})\
#     .findAll("td",{"class":re.compile('(/name/)+([a-z0-9A-Z])+(.*nmls_hd)'))
#
# for name in names:
#     name = name.string.rstrip("\n")
#     name_list.append(name)
#


r = requests.get(url)
# bs = BeautifulSoup(r.text)
bs=BeautifulSoup(r.text,"lxml")
table_body=bs.find('tbody')
rows = table_body.find_all('tr')
for row in rows:
    cols=row.find_all('td')
    cols=[x.text.strip() for x in cols]
    print (cols)




tr_elements = doc.xpath('//tr')
[len(T) for T in tr_elements[:12]]

tr_elements = doc.xpath('//tr')

col = []
col1=[]
i = 0
j=0
for t in tr_elements[0]:
    i += 1
    name = t.text_content()
    print(i, name)
    col.append((name, []))
    td_elements = doc.xpath('//td')
    for td in td_elements[0]:
        j += 1
        name1 = td.text_content()
        print(j, name1)
        col1.append((name, []))


Dict = {title: column for (title, column) in col}
df = pd.DataFrame(Dict)

for j in range(1, len(tr_elements)):
    # T is our j'th row
    T = tr_elements[j]

     if len(T) != 10:
        break

    i = 0
   for t in T.iterchildren():
        data = t.text_content()
       if i > 0:
           try:
                data = int(data)
            except:
                pass
        col[i][1].append(data)
       i += 1

Dict = {title: column for (title, column) in col}
df = pd.DataFrame(Dict)

df.head()
