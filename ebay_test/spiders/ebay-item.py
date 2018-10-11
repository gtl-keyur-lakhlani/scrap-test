import scrapy

class EbaySpider(scrapy.Spider):
    name = "ebay-item"

    def start_requests(self):
        urls = [
            #'https://www.ebay.com/itm/New-10-Ford-Massey-Ferguson-Perkins-Equipment-Key/202458766057?epid=7018695568&hash=item2f237b9ae9:g:SSwAAOSwDDxa5GnB',
            'https://www.ebay.com/b/Excavators/97122/bn_1511523'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        next_page_url = response.css('a[rel=next]::attr(href)').extract_first()
        yield{
            'link' : next_page_url
        }
            
      
    
                 
     
            
