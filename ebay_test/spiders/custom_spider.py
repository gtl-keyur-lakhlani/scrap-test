import scrapy
from scrapy.contrib.spiders import Rule
from scrapy.linkextractors import LinkExtractor
import re

from ebay_test.items import CustomfieldItem


class CustomSpider(scrapy.Spider):
    name = "custom"
    start_urls = ["https://www.ebay.com/b/Business-Industrial/12576/bn_1853744"]

    def parse(self, response):
        
        category_listing = response.xpath(".//*[@id='mainContent']/section[2]/div[2]/a/div/text()").extract()

        a = 0
        for cat in response.xpath("//*[@id='mainContent']/section[2]/div[2]/a//@href"):
            one_page = cat.extract()
            category = category_listing[a]
            a = a + 1
            yield scrapy.Request(one_page, callback=self.second_page, meta={'category': category})

    def second_page(self, response):
        category = response.meta['category']
        sub_category_listing = response.xpath(".//*[@id='mainContent']/section[2]/div[2]/a/div/text()").extract()

        b = 0
        for sub_cat in response.xpath(".//*[@id='mainContent']/section[2]/div[2]/a//@href"):
            other_page = sub_cat.extract()
            sub_category = sub_category_listing[b]
            b = b + 1
            yield scrapy.Request(other_page, callback=self.parse_content, meta={'category': category, 'sub_category': sub_category })

        # other_page = response.xpath(
            # ".//*[@id='mainContent']/section[2]/div[2]/a[1]//@href").extract_first()

        # yield scrapy.Request(other_page, callback=self.third_page)
        # yield scrapy.Request(other_page, callback=self.parse_content)

    def third_page(self, response):
        global company
        company = response.xpath(
            ".//*[@id='w6-xCarousel-x-carousel-items']/ul/li[1]/a/descendant::text()").extract_first()

        page = response.xpath(
            ".//*[@id='w6-xCarousel-x-carousel-items']/ul/li[1]/a/@href").extract_first()

        yield scrapy.Request(page, callback=self.parse_content)

    rules = (Rule(LinkExtractor(allow=(), restrict_xpaths=(
        '//a[contains(@class, "ebayui-pagination__control")]//@href',)), callback="parse_content", follow=True),)

    def parse_content(self, response):
        category = response.meta['category']
        sub_category = response.meta['sub_category']

        image = response.xpath(
            "//div[contains(@class, 's-item__image-wrapper')]//img[contains(@class, 's-item__image-img')]").extract()

        thumb_image = []

        for img in image:
            img_src = img.split('"')
            for thumb in img_src:
                if 'jpg' in thumb:
                    thumb_image.append(thumb)

        j = 0

        for href in response.xpath(
                "//div[contains(@class, 's-item__info clearfix')]/a[contains(@class, 's-item__link')]//@href"):

            url = href.extract()
            listing_url = url
            thumbnail_url = thumb_image[j]
            j = j + 1

            yield scrapy.Request(url, callback=self.parse_dir_contents, meta={'listing_url': listing_url,
                                                                              'thumbnail_url': thumbnail_url,
                                                                              'category': category, 'sub_category': sub_category})
       

    def parse_dir_contents(self, response):
        item = CustomfieldItem()

        # item['Category'] = category

        item['Category'] = response.meta['category']

        # item['Sub_Category'] = sub_category

        item['Sub_Category'] = response.meta['sub_category']

        # item['Company'] = company

        item['Listing_Title'] = response.xpath("//h1[contains(@id, 'itemTitle')]/text()").extract_first()

        item['Listing_URL'] = response.meta['listing_url']

        item['Thumbnail_URL'] = response.meta['thumbnail_url']

        item['Price'] = response.xpath(".//*[@id='prcIsum']/text()").extract_first()

        item['Vendor_Name'] = response.xpath(".//*[@id='mbgLink']/span/text()").extract_first()

        item['Vendor_URL'] = response.xpath(".//*[@id='mbgLink']//@href").extract_first()

        item['Images_URL'] = response.xpath(".//*[@id='vi_main_img_fs']/ul/li/table/tr/td/div/img/@src").extract()

        vendor_detail = response.xpath(".//*[@id='itemLocation']/div[2]/div/div[2]/span/text()").extract_first()

        if vendor_detail:
            vendor_detail = vendor_detail.split(',')
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

        else:
            vendor_detail = response.xpath(
                ".//*[@id='mainContent']/div[1]/table/tr[8]/td/div/div[2]/div[2]/text()").extract_first()

            if vendor_detail:
                vendor_detail = vendor_detail.split(',')
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
