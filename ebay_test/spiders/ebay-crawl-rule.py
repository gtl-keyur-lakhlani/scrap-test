import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.item import Item, Field

class MySpider(CrawlSpider):
    name = 'ebay.com'
    allowed_domains = ['ebay.com']
    start_urls = ['https://www.ebay.com/b/Business-Industrial/12576/bn_1853744']

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=('/itm/', )), callback='parse_item', follow= True),
    )

    def parse_item(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)
        #item = scrapy.Item()
        #item['name'] = response.xpath('//h1[@id="itemTitle"]/text()').extract()
        #item['name'] = response.xpath('/html/head/title/text()').extract()
        yield{
            'name' : response.css('h1[id="itemTitle"]::text').extract()
        }    
        #return item
