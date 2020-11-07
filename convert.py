import feedparser
import PyRSS2Gen
import os
from flask import Flask
from googletrans import Translator
from bs4 import BeautifulSoup

app = Flask(__name__)
translator = Translator()


def parseRSS(rss_url):
    return feedparser.parse(rss_url)


def getHeadlines(rss_url):
    headlines = []

    feed = parseRSS(rss_url)
    for newsitem in feed['items']:
        print(newsitem)
        iLink = newsitem['link']
        #translated = translator.translate(newsitem['title'], src='en', dest='te')
        #if translated is None:
        translated = newsitem['title']
        iTitle = translated
        #translated = translator.translate(newsitem['description'], src='en', dest='te')
        #if translated is None:
        translated = newsitem['description']
        iDescription = translated
        iPublished = newsitem['published']
        iPublishedParse = newsitem['published_parsed']
        iEnclosure = newsitem['links']
        headlines.append(
            [iLink, iTitle, iDescription, iEnclosure[1].href, iEnclosure[1].length, iEnclosure[1].type, iPublished,
             iPublishedParse])
    return headlines


@app.route('/')
def fetch():
    allheadlines = []

    newsurls = {
        'googlenews': 'https://www.nasa.gov/rss/dyn/lg_image_of_the_day.rss',
    }

    for key, url in newsurls.items():
        allheadlines.extend(getHeadlines(url))

    rss = PyRSS2Gen.RSS2(
        title='తెలుగులో నాసా ఇమేజ్ ఆఫ్ ది డే',
        link='https://www.nasa.gov/rss/dyn/lg_image_of_the_day.rss',
        description='తాజా నాసా ఇమేజ్ ఆఫ్ ది డే చిత్రం తెలుగులో',
        language='te-ind',
        items=[],
    )

    for hl in allheadlines:
        rss.items.append(PyRSS2Gen.RSSItem(
            title=hl[1],
            link=hl[0],
            description=hl[2],
            enclosure=PyRSS2Gen.Enclosure(url=hl[3], length=hl[4], type=hl[5]),
            pubDate=hl[6],
        ))

    # rss.write_xml(open("తెలుగులో నాసా ఇమేజ్ ఆఫ్ ది డే.xml", "w", encoding="utf-16"))
    soup = BeautifulSoup(rss.to_xml(encoding="utf-16"), 'lxml')
    return soup.prettify()


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)