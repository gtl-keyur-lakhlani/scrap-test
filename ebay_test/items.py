# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CustomfieldItem(scrapy.Item):
    # define the fields for your item here like:
    Category = scrapy.Field()
    Sub_Category = scrapy.Field()
    # Company = scrapy.Field()
    Listing_Title = scrapy.Field()
    Year = scrapy.Field()
    ExcavatorType = scrapy.Field()
    SerialNumber = scrapy.Field()
    Make = scrapy.Field()
    Model = scrapy.Field()
    CustomBundle = scrapy.Field()
    UPC = scrapy.Field()
    Hours = scrapy.Field()
    Price = scrapy.Field()
    Vendor_Name = scrapy.Field()
    Vendor_Country = scrapy.Field()
    Vendor_State = scrapy.Field()
    Vendor_City = scrapy.Field()
    Vendor_URL = scrapy.Field()
    Images_URL = scrapy.Field()
    Thumbnail_URL = scrapy.Field()
    Listing_URL = scrapy.Field()
