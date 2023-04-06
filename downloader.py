import urllib.request
from bs4 import BeautifulSoup

url = 'http://nzz.ch'
data = urllib.request.urlopen(url).read()
soup = BeautifulSoup(data, "html.parser")

headlines_nzz = soup.find_all(['h2'])

for i in headlines_nzz:
    print(i.text.strip())

