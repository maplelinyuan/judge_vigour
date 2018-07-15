# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QiutanOriginOddsItem_total(scrapy.Item):
# class QiutanOriginOddsItem(scrapy.Item):
    # define the fields for your item here like:
    match_id = scrapy.Field()
    bet365_home_origin_odd = scrapy.Field()     # bet365初盘主赔
    bet365_draw_origin_odd = scrapy.Field()     # bet365初盘平赔
    bet365_away_origin_odd = scrapy.Field()     # bet365初盘客赔
    bet365_home_last_odd = scrapy.Field()       # bet365终盘主赔
    bet365_draw_last_odd = scrapy.Field()       # bet365终盘平赔
    bet365_away_last_odd = scrapy.Field()       # bet365终盘客赔
    bet365_origin_home_handicap = scrapy.Field()        # bet365初盘上盘赔
    bet365_origin_handicap = scrapy.Field()     # bet365初盘盘口
    bet365_origin_away_handicap = scrapy.Field()    # bet365初盘下盘赔
    bet365_last_home_handicap = scrapy.Field()      # bet365终盘上盘赔
    bet365_last_handicap = scrapy.Field()       # bet365钟盘盘口
    bet365_last_away_handicap = scrapy.Field()      # bet365钟盘下盘赔
    bet365_origin_over = scrapy.Field()     # bet365初盘大球赔
    bet365_origin_goal_handicap = scrapy.Field()        # bet365初盘大小球盘口
    bet365_origin_under = scrapy.Field()        # bet365初盘小球赔
    bet365_last_over = scrapy.Field()       # bet365终盘大球赔
    bet365_last_goal_handicap = scrapy.Field()      # bet365终盘大小球盘口
    bet365_last_under = scrapy.Field()      # bet365终盘小球赔
    ladbrokes_home_origin_odd = scrapy.Field()  # ladbrokes初盘主赔
    ladbrokes_draw_origin_odd = scrapy.Field()  # ladbrokes初盘平赔
    ladbrokes_away_origin_odd = scrapy.Field()  # ladbrokes初盘客赔
    ladbrokes_home_last_odd = scrapy.Field()  # ladbrokes终盘主赔
    ladbrokes_draw_last_odd = scrapy.Field()  # ladbrokes终盘平赔
    ladbrokes_away_last_odd = scrapy.Field()  # ladbrokes终盘客赔
    ladbrokes_origin_home_handicap = scrapy.Field()  # ladbrokes初盘上盘赔
    ladbrokes_origin_handicap = scrapy.Field()  # ladbrokes初盘盘口
    ladbrokes_origin_away_handicap = scrapy.Field()  # ladbrokes初盘下盘赔
    ladbrokes_last_home_handicap = scrapy.Field()  # ladbrokes终盘上盘赔
    ladbrokes_last_handicap = scrapy.Field()  # ladbrokes钟盘盘口
    ladbrokes_last_away_handicap = scrapy.Field()  # ladbrokes钟盘下盘赔
    ladbrokes_origin_over = scrapy.Field()  # ladbrokes初盘大球赔
    ladbrokes_origin_goal_handicap = scrapy.Field()  # ladbrokes初盘大小球盘口
    ladbrokes_origin_under = scrapy.Field()  # ladbrokes初盘小球赔
    ladbrokes_last_over = scrapy.Field()  # ladbrokes终盘大球赔
    ladbrokes_last_goal_handicap = scrapy.Field()  # ladbrokes终盘大小球盘口
    ladbrokes_last_under = scrapy.Field()  # ladbrokes终盘小球赔
    home_total_match = scrapy.Field()       # 主队总比赛
    home_total_point = scrapy.Field()       # 主队总积分
    home_win_pro = scrapy.Field()       # 主队主场胜率
    away_total_match = scrapy.Field()       # 客队总比赛
    away_total_point = scrapy.Field()       # 客队总积分
    away_win_pro = scrapy.Field()       # 客队客场胜率
    home_latest_win_pro = scrapy.Field()       # 主队近况胜率
    home_latest_draw_pro = scrapy.Field()       # 主队近况平率
    home_latest_away_pro = scrapy.Field()       # 主队近况负率
    home_latest_win_handicap_pro = scrapy.Field()       # 主队近况赢盘率
    home_latest_big_goal_pro = scrapy.Field()       # 主队近况大球率
    away_latest_win_pro = scrapy.Field()  # 客队近况胜率
    away_latest_draw_pro = scrapy.Field()  # 客队近况平率
    away_latest_away_pro = scrapy.Field()  # 客队近况负率
    away_latest_win_handicap_pro = scrapy.Field()  # 客队近况赢盘率
    away_latest_big_goal_pro = scrapy.Field()  # 客队近况大球率
    jiaofeng_home_pro = scrapy.Field()  # 交锋310概率
    jiaofeng_draw_pro = scrapy.Field()
    jiaofeng_away_pro = scrapy.Field()
    jiaofeng_win_handicap_pro = scrapy.Field()      # 交锋赢盘率
    jiaofeng_big_goal_pro = scrapy.Field()      # 交锋大球率
