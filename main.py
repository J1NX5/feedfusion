import feedparser

def fetch_rss_feed(url):

    feed = feedparser.parse(url)
    print(feed.entries)


# Has this keys: 'bozo', 'entries', 'feed', 'headers', 'etag', 'href', 'status', 'encoding', 'version', 'namespaces'
rss_url = "https://www.wallstreet-online.de/rss/nachrichten-aktien-indizes.xml"


if __name__ == '__main__':
    fetch_rss_feed(rss_url)