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
           listing_url = response.url
           thumbnail_url = items.css('img.s-item__image-img::attr(src)').extract_first()
           categories = items.css('.b-breadcrumb__text').extract()
           category = ''
           sub_category = ''
           if (len(categories) > 0):
               category = categories(len(categories)-1)
               sub_category = categories(len(categories)-2)
               
           if detail_href:
               yield  scrapy.Request(url=detail_href, callback=self.parse_detail, meta={'listing_url': listing_url,
                                                                              'thumbnail_url': thumbnail_url,
                                                                              'category': category, 'sub_category': sub_category})
        
        next_page_url = response.css('a[rel=next]::attr(href)').extract_first()
        if next_page_url:
               yield  scrapy.Request(url=next_page_url, callback=self.parse) 
                 
    
    def parse_detail(self, response):
         
        #yield{
        #    'name' : response.css('h1.it-ttl::text').extract_first().replace('Details about', '').strip()
        #}    
        item = CustomfieldItem()

        # item['Category'] = category
        item['Category'] = ''
        if response.meta['category']:
            item['Category'] = response.meta['category']

        # item['Sub_Category'] = sub_category
        item['Sub_Category'] = ''
        if response.meta['sub_category']:
            item['Sub_Category'] = response.meta['sub_category']

        # item['Company'] = company

        item['Listing_Title'] = response.xpath(
            "//h1[contains(@id, 'itemTitle')]/text()").extract_first()

        item['Listing_URL'] = ''
        if response.meta['listing_url']:
            item['Listing_URL'] = response.meta['listing_url']

        item['Thumbnail_URL'] = ''
        if response.meta['thumbnail_url']:
            item['Thumbnail_URL'] = response.meta['thumbnail_url']

        item['Price'] = response.xpath(".//*[@id='prcIsum']/text()").extract_first()

        item['Vendor_Name'] = response.xpath(".//*[@id='mbgLink']/span/text()").extract_first()

        item['Vendor_URL'] = response.xpath(
            ".//*[@id='mbgLink']//@href").extract_first()

        item['Images_URL'] = response.xpath(
            ".//*[@id='vi_main_img_fs']/ul/li/table/tr/td/div/img/@src").extract()

        vendor_detail = response.xpath(
            ".//*[@id='itemLocation']/div[2]/div/div[2]/span/text()").extract_first().split(
            ',')

        details = len(vendor_detail)

        if details:
            if details == 3:
                item['Vendor_City'] = vendor_detail[0]
                item['Vendor_State'] = vendor_detail[1]
                item['Vendor_Country'] = vendor_detail[2]
            elif details == 2:
                item['Vendor_State'] = vendor_detail[0]
                item['Vendor_Country'] = vendor_detail[1]
            else:
                item['Vendor_Country'] = vendor_detail[0]

        parameter_array = ['ExcavatorType', 'SerialNumber', 'Make', 'Model', 'CustomBundle', 'UPC', 'Hours']

        model_data = response.xpath(
            "//div[contains(@id, 'viTabs_0_is')]//div[contains(@class, 'section')]//table/tr/descendant::text()").extract()

        table_data = [line for line in model_data if line.strip() != '']

        table_param = []

        for detail in table_data:
            detail = ''.join(detail.split())
            detail = detail.replace(':', '')
            table_param.append(detail)

        i = 0

        while i != len(table_param):
            for value in parameter_array:
                if table_param[i] == value:
                    i = i + 1
                    item[value] = table_param[i]
                if 'Year' in table_param[i]:
                    i = i + 1
                    item['Year'] = table_param[i]
            i = i + 1

        yield item
           
        
