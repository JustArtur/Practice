import requests
from bs4 import BeautifulSoup


def get_episod_info(episod):
    return f'{season1[episod][2]} Episod direcred by {season1[episod][0]} was watched by {season1[episod][1]} milliom viewers in USA'


tittle = []
dirested_by = []
viewers = []
season1 = {}
count = 1

resp = requests.get("https://en.wikipedia.org/wiki/List_of_Rick_and_Morty_episodes").content
bs = BeautifulSoup(resp, 'lxml')
my_table = bs.find_all('table', {'class':'wikitable plainrowheaders wikiepisodetable'})
my_rows = my_table[0].find_all('tr')

tittle.append(my_rows[0].find_all('th')[2].get_text())
dirested_by.append((my_rows[0].find_all('th')[3].get_text()))
viewers.append((my_rows[0].find_all('th')[6].get_text()))

for row in my_rows[1:]:
    r = row.find_all('td')
    tittle.append(r[1].get_text())
    dirested_by.append(r[2].get_text())
    viewers.append(float(r[5].get_text().split('[')[0]))
    season1[tittle[count]] = [dirested_by[count], viewers[count], count]
    print(get_episod_info(tittle[count]))
    count += 1



