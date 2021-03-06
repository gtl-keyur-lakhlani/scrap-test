import scrapy
import re

from ebay_test.items import CustomfieldItem


class CustomSpider(scrapy.Spider):
    name = "test_custom"
    start_urls = ["https://www.ebay.com/b/Business-Industrial/12576/bn_1853744"]

    def parse(self, response):
        global category
        category = response.xpath(
            "//*[@id='mainContent']/section[2]/div[2]/a[1]/descendant::text()").extract_first()

        one_page = response.xpath(
            "//*[@id='mainContent']/section[2]/div[2]/a[1]//@href").extract_first()

        yield scrapy.Request(one_page, callback=self.second_page)

    def second_page(self, response):
        global sub_category
        sub_category = response.xpath(
            ".//*[@id='mainContent']/section[2]/div[2]/a[1]/descendant::text()").extract_first()

        other_page = response.xpath(
            ".//*[@id='mainContent']/section[2]/div[2]/a[1]//@href").extract_first()

        yield scrapy.Request(other_page, callback=self.third_page)

    def third_page(self, response):
        global company
        company = response.xpath(
            ".//*[@id='w6-xCarousel-x-carousel-items']/ul/li[1]/a/descendant::text()").extract_first()

        page = response.xpath(
            ".//*[@id='w6-xCarousel-x-carousel-items']/ul/li[1]/a/@href").extract_first()

        yield scrapy.Request(page, callback=self.parse_content)

    def parse_content(self, response):
        

        next_page = response.xpath(".//*[@id='w7-w1']/a[2]//@href").extract_first()
        yield {
            'next_page' : next_page
        }    
        

    def parse_dir_contents(self, response):
        item = CustomfieldItem()

        item['Category'] = category

        item['Sub_Category'] = sub_category

        item['Company'] = company

        item['Listing_Title'] = response.xpath(
            "//h1[contains(@id, 'itemTitle')]/text()").extract_first()

        item['Listing_URL'] = response.meta['listing_url']

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
