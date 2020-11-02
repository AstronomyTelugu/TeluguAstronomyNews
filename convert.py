import feedparser
import datetime
import PyRSS2Gen
from googletrans import Translator

translator = Translator()


def parseRSS(rss_url):
    return feedparser.parse(rss_url)


def getHeadlines(rss_url):
    headlines = []

    feed = parseRSS(rss_url)
    for newsitem in feed['items']:
        print(newsitem)
        iLink = newsitem['link']
        translated = translator.translate(newsitem['title'], src='en', dest='te')
        iTitle = translated.text
        translated = translator.translate(newsitem['description'], src='en', dest='te')
        iDescription = translated.text
        iPublished = newsitem['published']
        iPublishedParse = newsitem['published_parsed']
        iEnclosure = newsitem['links']
        headlines.append([iLink, iTitle, iDescription, iEnclosure[1].href, iEnclosure[1].length, iEnclosure[1].type, iPublished, iPublishedParse])
    return headlines


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
        pubDate = hl[6],
    ))

rss.write_xml(open("pyrss2gen.xml", "w", encoding="utf-16"))
