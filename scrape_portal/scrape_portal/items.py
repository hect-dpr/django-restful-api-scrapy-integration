# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NSEItem(scrapy.Item):
    # define the fields for your news relevant information
    symbol          =   scrapy.Field()
    open            =   scrapy.Field()
    high            =   scrapy.Field()
    low             =   scrapy.Field()
    ltp             =   scrapy.Field()
    chng            =   scrapy.Field()
    pcnt_chng       =   scrapy.Field()
    volume          =   scrapy.Field()
    turnover        =   scrapy.Field()
    ftwh            =   scrapy.Field()
    ftwl            =   scrapy.Field()
    tsfd_pcnt_chng  =   scrapy.Field()
    td_pcnt_chng    =   scrapy.Field()
