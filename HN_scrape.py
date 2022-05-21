import requests
from bs4 import BeautifulSoup
import time
import sys

# .titlelink instead of .storylink
page_select = sys.argv[1]

res = requests.get(f'https://news.ycombinator.com/news?p={page_select}')
soup = BeautifulSoup(res.text, 'html.parser')
links = (soup.select('.titlelink'))
subtext = soup.select('.subtext')


def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k: k['votes'], reverse=True)


def create_custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):

        title = item.getText()
        href = item.get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points})
                print('\n')
    return sort_stories_by_votes(hn)


timestr = time.strftime("%Y%m%d")


with open(f'./HN_topStories_{timestr}_page{page_select}.txt', 'w') as f:
    f.write(str(create_custom_hn(links,subtext)))


