from urllib import urlopen
from urlparse import urljoin
from urllib2 import Request, build_opener
from BeautifulSoup import BeautifulSoup

import time
from OrderedSet import OrderedSet

# Time gap btw page fetches
PAGE_TIME_RELAY = 0.025

def crawl(seeds, urls_count=100):
  '''
  Input:
    seeds: List of urls from where crawling starts
    urls_count: Minimul Limit of urls to the gathered first
  Output:
    frontier: OrderedSet of urls
  '''
    frontier = seeds
    visited_urls = OrderedSet()
    for crawl_url in frontier:
        print "Crawling: %s " % crawl_url
        visited_urls.add(crawl_url)
        try:
            resp = urlopen(crawl_url)
        except:
            print "...crawl failed:"
            continue
        content_type = resp.info().get('Content-Type')
        if not content_type.startswith('text/html'):
            print "...skipping non html page"
            continue
        contents = repr(resp.read())
        soup = BeautifulSoup(contents)
        links = OrderedSet(soup('a'))
        discovered_urls = OrderedSet()
        for link in links:
            if link.has_key('href'):
                url = urljoin( crawl_url, link['href'])
                if url.startswith('http') and\
                    url not in frontier and\
                    url not in discovered_urls:
                    discovered_urls.add(url)
        frontier += discovered_urls
        time.sleep(PAGE_TIME_RELAY)
        if len(frontier) > urls_count:
          return frontier

seeds = ['http://python.org/']
