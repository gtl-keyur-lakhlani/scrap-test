import scrapy

class EbaySpider(scrapy.Spider):
    name = "ebay"

    def start_requests(self):
        urls = [
            'https://www.ebay.com/b/Business-Industrial/12576/bn_1853744',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for href in response.css('div.b-visualnav__grid a::attr(href)'):
             yield scrapy.Request(url=href.extract(), callback=self.parse)

        item_list_page = 0
        for items in response.css('li.s-item'):
           item_list_page = 1
           detail_href = items.css('a.s-item__link::attr(href)').extract_first()
           if(detail_href != ''):
               yield  scrapy.Request(url=detail_href, callback=self.parse_detail)
        
        next_page_url = response.css('a[rel=next]::attr(href)').extract_first()
        if(next_page_url != '' and item_list_page == 1):
               yield  scrapy.Request(url=next_page_url, callback=self.parse) 
                 
    
    def parse_detail(self, response):
         
        yield{
            'name' : response.css('h1.it-ttl::text').extract_first().replace('Details about', '').strip()
        }    

           
        
