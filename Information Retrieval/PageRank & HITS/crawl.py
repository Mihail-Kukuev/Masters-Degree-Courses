import pickle
import re

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup

pages_dict = {}


class WikiPage:
    def __init__(self):
        self.url = ''
        self.title = ''
        self.links = []
        self.snippet = ''


class WikiSpider(CrawlSpider):
    name = 'wiki_spider'

    custom_settings = {
        'CLOSESPIDER_PAGECOUNT': 10000,
        'DEPTH_PRIORITY': 1,
        'SCHEDULER_DISK_QUEUE': 'scrapy.squeues.PickleFifoDiskQueue',
        'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue',
        'LOG_LEVEL': 'ERROR',
    }

    start_urls = [
        "https://en.wikipedia.org/wiki/Stephen_Hawking",
        "https://en.wikipedia.org/wiki/Albert_Einstein",
        "https://en.wikipedia.org/wiki/AC/DC",
        "https://en.wikipedia.org/wiki/Kiss",
        "https://en.wikipedia.org/wiki/Slade"
    ]

    header_selector = 'h1#firstHeading.firstHeading::text,h1#firstHeading.firstHeading > *::text'
    body_link_selector = 'div#mw-content-text.mw-content-ltr a::attr("href")'
    allowed_re = re.compile('https://.+\.wikipedia\.org/wiki/'
                            '(?!((File|Talk|Category|Portal|Special|Wikipedia'
                            '|Help|Draft|Template|Free_Content|Template_talk):|Main_Page)).+')

    extractor = LinkExtractor(allow=allowed_re,
                              deny=('.*#.*',),
                              restrict_xpaths='(//div[@id="mw-content-text"]//a)[position() < 100]')

    rules = (Rule(extractor, callback='parse_wiki_page', follow=True),)

    visited_urls = set()

    def parse_wiki_page(self, response):
        if response.url not in self.visited_urls:
            self.visited_urls.add(response.url)
        else:
            return

        page = WikiPage()

        page.url = response.url

        title = response.css(self.header_selector)
        page.title = title.extract_first().encode('utf-8') if title else ''

        page_links = []
        for link in response.css(self.body_link_selector).extract():
            if '#' in link:
                continue
            next_url = response.urljoin(link)
            if self.allowed_re.match(next_url):
                page_links.append(next_url)

        page.links = page_links[:100]

        description = response.xpath('//div[@id="mw-content-text"]/div[1]/p[1]').extract_first()
        page.snippet = BeautifulSoup(description, "lxml").text[:255].encode('utf-8') + "..." if description else ''

        pages_dict[page.url] = page


def crawl_wiki():
    pages_dict.clear()
    process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
    process.crawl(WikiSpider)
    process.start()

    dump_file = open('wiki_pages.bin', 'wb')
    pickle.dump(pages_dict, dump_file)
    dump_file.close()


if __name__ == '__main__':
    crawl_wiki()
