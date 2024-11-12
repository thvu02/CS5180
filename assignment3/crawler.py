from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
import regex as re
from pymongo import MongoClient
import pprint

class Frontier:
    def __init__(self, baseurl):
        self.frontier = [baseurl] if baseurl is not None else []

    def done(self):
        return len(self.frontier) == 0
    
    def nextURL(self):
        return self.frontier.pop(0)
    
    def addURL(self, url):
        self.frontier.append(url)
    
class Crawler:
    def __init__(self, baseurl, target):
        self.frontier = Frontier(baseurl)
        self.visited = set()
        self.target = target
        self.target_found = False # really just here to met psuedo code requirements
        db = self.connectToMongoDB()
        self.pages = db['pages']
    
    def connectToMongoDB(self):
        DB_NAME = "CPP"
        DB_HOST = "localhost"
        DB_PORT = 27017
        try:
            client = MongoClient(host=DB_HOST, port=DB_PORT)
            db = client[DB_NAME]
            return db
        except:
            print("Database not connected successfully")

    def debug(self):
        for document in self.pages.find():
            pprint.pprint(document)

    def retrievHTML(self, url):
        try:
            html = urlopen(url)
        except HTTPError as e:
            print(e)
        except URLError as e:
            print('The server could not be found!')
        else:
            self.visited.add(url)
            return html

    def storePage(self, url, html):
        entry = {
            'url': url,
            'html': html
        }
        self.pages.insert_one(entry)
    
    def parseForCriteria(self, bs):
        if bs.find('h1', {'class': 'cpp-h1'}) == None:
            return False
        else:
            return bs.find('h1', {'class': 'cpp-h1'}).get_text() == 'Permanent Faculty'
    
    def target_page(self, parseForCriteria):
        return parseForCriteria

    def flagTargetPage(self, url):
        print(f"Target page found at {url}")
        self.target_found = True

    def clear_frontier(self):
        self.frontier = Frontier(None)

    def parseForLinks(self, bs):
        # find all links with .html or .shtml'))
        discovered_links = [item['href'] for item in bs.find_all('a', {'class': 'nav-link'}, href=re.compile('.*(.html|.shtml)$', re.IGNORECASE))]
        # change all relative links into full addresses
        for i, item in enumerate(discovered_links):
            # CASE: relative address
            if item.startswith('/'):
                discovered_links[i] = "https://www.cpp.edu" + item
            # CASE: full address
            elif item.startswith('http'):
                continue # do nothing
        return discovered_links
    
    def crawl(self):
        while not self.frontier.done():
            url = self.frontier.nextURL()
            html = self.retrievHTML(url)
            # for some reason only the initial call of BeautifulSoup(html, 'html.parser')
            # returns the HTML content, so do it here and pass bs to funcs instead of html
            bs = BeautifulSoup(html, 'html.parser')            
            self.storePage(url, bs.prettify())
            if self.target_page(self.parseForCriteria(bs)):
                self.flagTargetPage(self.target)
                self.clear_frontier()
            else:
                for item in self.parseForLinks(bs):
                    if item not in self.visited:
                        self.frontier.addURL(item)

if __name__ == '__main__':
    crawler = Crawler('https://www.cpp.edu/sci/computer-science/', 'https://www.cpp.edu/sci/computer-science/faculty-and-staff/permanent-faculty.shtml')
    crawler.crawl()
    print("Crawling completed!")