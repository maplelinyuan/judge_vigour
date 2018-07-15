# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QiutanOriginOddsItem(scrapy.Item):
    # define the fields for your item here like:
    match_id = scrapy.Field()
    Crown_origin_over = scrapy.Field()     # Crown初盘大球赔
    Crown_origin_goal_handicap = scrapy.Field()        # Crown初盘大小球盘口
    Crown_origin_under = scrapy.Field()        # Crown初盘小球赔
    Crown_last_over = scrapy.Field()       # Crown终盘大球赔
    Crown_last_goal_handicap = scrapy.Field()      # Crown终盘大小球盘口
    Crown_last_under = scrapy.Field()      # Crown终盘小球赔
    bet365_origin_over = scrapy.Field()     # bet365初盘大球赔
    bet365_origin_goal_handicap = scrapy.Field()        # bet365初盘大小球盘口
    bet365_origin_under = scrapy.Field()        # bet365初盘小球赔
    bet365_last_over = scrapy.Field()       # bet365终盘大球赔
    bet365_last_goal_handicap = scrapy.Field()      # bet365终盘大小球盘口
    bet365_last_under = scrapy.Field()      # bet365终盘小球赔
    yishengbo_origin_over = scrapy.Field()     # yishengbo初盘大球赔
    yishengbo_origin_goal_handicap = scrapy.Field()        # yishengbo初盘大小球盘口
    yishengbo_origin_under = scrapy.Field()        # yishengbo初盘小球赔
    yishengbo_last_over = scrapy.Field()       # yishengbo终盘大球赔
    yishengbo_last_goal_handicap = scrapy.Field()      # yishengbo终盘大小球盘口
    yishengbo_last_under = scrapy.Field()      # yishengbo终盘小球赔
    weide_origin_over = scrapy.Field()     # weide初盘大球赔
    weide_origin_goal_handicap = scrapy.Field()        # weide初盘大小球盘口
    weide_origin_under = scrapy.Field()        # weide初盘小球赔
    weide_last_over = scrapy.Field()       # weide终盘大球赔
    weide_last_goal_handicap = scrapy.Field()      # weide终盘大小球盘口
    weide_last_under = scrapy.Field()      # weide终盘小球赔
    mingsheng_origin_over = scrapy.Field()     # mingsheng初盘大球赔
    mingsheng_origin_goal_handicap = scrapy.Field()        # mingsheng初盘大小球盘口
    mingsheng_origin_under = scrapy.Field()        # mingsheng初盘小球赔
    mingsheng_last_over = scrapy.Field()       # mingsheng终盘大球赔
    mingsheng_last_goal_handicap = scrapy.Field()      # mingsheng终盘大小球盘口
    mingsheng_last_under = scrapy.Field()      # mingsheng终盘小球赔
    bet10_origin_over = scrapy.Field()     # bet10初盘大球赔
    bet10_origin_goal_handicap = scrapy.Field()        # bet10初盘大小球盘口
    bet10_origin_under = scrapy.Field()        # bet10初盘小球赔
    bet10_last_over = scrapy.Field()       # bet10终盘大球赔
    bet10_last_goal_handicap = scrapy.Field()      # bet10终盘大小球盘口
    bet10_last_under = scrapy.Field()      # bet10终盘小球赔
    jinbaobo_origin_over = scrapy.Field()     # jinbaobo初盘大球赔
    jinbaobo_origin_goal_handicap = scrapy.Field()        # jinbaobo初盘大小球盘口
    jinbaobo_origin_under = scrapy.Field()        # jinbaobo初盘小球赔
    jinbaobo_last_over = scrapy.Field()       # jinbaobo终盘大球赔
    jinbaobo_last_goal_handicap = scrapy.Field()      # jinbaobo终盘大小球盘口
    jinbaobo_last_under = scrapy.Field()      # jinbaobo终盘小球赔
    bet12_origin_over = scrapy.Field()     # bet12初盘大球赔
    bet12_origin_goal_handicap = scrapy.Field()        # bet12初盘大小球盘口
    bet12_origin_under = scrapy.Field()        # bet12初盘小球赔
    bet12_last_over = scrapy.Field()       # bet12终盘大球赔
    bet12_last_goal_handicap = scrapy.Field()      # bet12终盘大小球盘口
    bet12_last_under = scrapy.Field()      # bet12终盘小球赔
    liji_origin_over = scrapy.Field()     # liji初盘大球赔
    liji_origin_goal_handicap = scrapy.Field()        # liji初盘大小球盘口
    liji_origin_under = scrapy.Field()        # liji初盘小球赔
    liji_last_over = scrapy.Field()       # liji终盘大球赔
    liji_last_goal_handicap = scrapy.Field()      # liji终盘大小球盘口
    liji_last_under = scrapy.Field()      # liji终盘小球赔
    yinghe_origin_over = scrapy.Field()     # yinghe初盘大球赔
    yinghe_origin_goal_handicap = scrapy.Field()        # yinghe初盘大小球盘口
    yinghe_origin_under = scrapy.Field()        # yinghe初盘小球赔
    yinghe_last_over = scrapy.Field()       # yinghe终盘大球赔
    yinghe_last_goal_handicap = scrapy.Field()      # yinghe终盘大小球盘口
    yinghe_last_under = scrapy.Field()      # yinghe终盘小球赔
    bet18_origin_over = scrapy.Field()     # bet18初盘大球赔
    bet18_origin_goal_handicap = scrapy.Field()        # bet18初盘大小球盘口
    bet18_origin_under = scrapy.Field()        # bet18初盘小球赔
    bet18_last_over = scrapy.Field()       # bet18终盘大球赔
    bet18_last_goal_handicap = scrapy.Field()      # bet18终盘大小球盘口
    bet18_last_under = scrapy.Field()      # bet18终盘小球赔
    ladbrokes_origin_over = scrapy.Field()     # ladbrokes初盘大球赔
    ladbrokes_origin_goal_handicap = scrapy.Field()        # ladbrokes初盘大小球盘口
    ladbrokes_origin_under = scrapy.Field()        # ladbrokes初盘小球赔
    ladbrokes_last_over = scrapy.Field()       # ladbrokes终盘大球赔
    ladbrokes_last_goal_handicap = scrapy.Field()      # ladbrokes终盘大小球盘口
    ladbrokes_last_under = scrapy.Field()      # ladbrokes终盘小球赔
