import feedparser
import urllib3
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urlunparse

FEEDS_TO_PULL = [
    ('googlenews', 'https://tinyurl.com/y38qbvfa', True),
]


def sortitem(val):
    return int(
        "{:0>4d}{:0>2d}{:0>2d}{:0>2d}{:0>2d}{:0>2d}".format(val[5][0], val[5][1], val[5][2], val[5][3], val[5][4],
                                                            val[5][5]))


def resolve_image(url):
    urlInfo = urlparse(url)
    urlBase = urlInfo.scheme + '://' + urlInfo.netloc
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="html.parser")
    tag = soup.find('meta', attrs={'property': 'og:image'})
    if tag is not None and 'content' in tag.attrs:
        return urljoin(urlBase, tag['content'])

    tag = soup.find('link', attrs={'rel': 'shortcut icon'})
    if tag is not None and 'href' in tag.attrs:
        return urljoin(urlBase, tag['href'])

    tag = soup.find('img')
    if tag is not None and 'src' in tag.attrs:
        return urljoin(urlBase, tag['src'])
    return None


def get_items():
    items = []
    for feed in FEEDS_TO_PULL:
        parsed = feedparser.parse(feed[1])

        feeditems = []
        i = 0
        for item in parsed.entries[:25]:
            i = i + 1
            iLink = item['link']
            iTitle = item['title']
            iDescription = item['description']
            iSource = item['source'].title
            iPublished = item['published']
            iPublishedParse = item['published_parsed']
            try:
                iImage = resolve_image(iLink)
            except Exception as e:
                iImage = ' '
            print(i)
            feeditems.append([iLink, iTitle, iImage, iSource, iPublished, iPublishedParse])
            feeditems.sort(key=sortitem, reverse=True)

        items += feeditems
    return sorted(items, key=sortitem, reverse=True)


feeditems = get_items()
