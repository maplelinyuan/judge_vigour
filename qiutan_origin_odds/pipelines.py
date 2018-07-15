# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
import datetime, time
import pdb
import traceback

class QiutanOriginOddsPipeline(object):
    def __init__(self):
        # 链接数据库
        self.mongo_client = MongoClient(host='localhost', port=27019)
        # self.mongo_client.admin.authenticate(settings['MINGO_USER'], settings['MONGO_PSW'])     #如果有账户密码

    def process_item(self, item, spider):
        match_id = item['match_id']
        # Crown_origin_over = item['Crown_origin_over']
        # Crown_origin_goal_handicap = item['Crown_origin_goal_handicap']
        # Crown_origin_under = item['Crown_origin_under']
        # Crown_last_over = item['Crown_last_over']
        # Crown_last_goal_handicap = item['Crown_last_goal_handicap']
        # Crown_last_under = item['Crown_last_under']
        bet365_origin_over = item['bet365_origin_over']
        bet365_origin_goal_handicap = item['bet365_origin_goal_handicap']
        bet365_origin_under = item['bet365_origin_under']
        bet365_last_over = item['bet365_last_over']
        bet365_last_goal_handicap = item['bet365_last_goal_handicap']
        bet365_last_under = item['bet365_last_under']
        yishengbo_origin_over = item['yishengbo_origin_over']
        yishengbo_origin_goal_handicap = item['yishengbo_origin_goal_handicap']
        yishengbo_origin_under = item['yishengbo_origin_under']
        yishengbo_last_over = item['yishengbo_last_over']
        yishengbo_last_goal_handicap = item['yishengbo_last_goal_handicap']
        yishengbo_last_under = item['yishengbo_last_under']
        weide_origin_over = item['weide_origin_over']
        weide_origin_goal_handicap = item['weide_origin_goal_handicap']
        weide_origin_under = item['weide_origin_under']
        weide_last_over = item['weide_last_over']
        weide_last_goal_handicap = item['weide_last_goal_handicap']
        weide_last_under = item['weide_last_under']
        mingsheng_origin_over = item['mingsheng_origin_over']
        mingsheng_origin_goal_handicap = item['mingsheng_origin_goal_handicap']
        mingsheng_origin_under = item['mingsheng_origin_under']
        mingsheng_last_over = item['mingsheng_last_over']
        mingsheng_last_goal_handicap = item['mingsheng_last_goal_handicap']
        mingsheng_last_under = item['mingsheng_last_under']
        bet10_origin_over = item['bet10_origin_over']
        bet10_origin_goal_handicap = item['bet10_origin_goal_handicap']
        bet10_origin_under = item['bet10_origin_under']
        bet10_last_over = item['bet10_last_over']
        bet10_last_goal_handicap = item['bet10_last_goal_handicap']
        bet10_last_under = item['bet10_last_under']
        jinbaobo_origin_over = item['jinbaobo_origin_over']
        jinbaobo_origin_goal_handicap = item['jinbaobo_origin_goal_handicap']
        jinbaobo_origin_under = item['jinbaobo_origin_under']
        jinbaobo_last_over = item['jinbaobo_last_over']
        jinbaobo_last_goal_handicap = item['jinbaobo_last_goal_handicap']
        jinbaobo_last_under = item['jinbaobo_last_under']
        bet12_origin_over = item['bet12_origin_over']
        bet12_origin_goal_handicap = item['bet12_origin_goal_handicap']
        bet12_origin_under = item['bet12_origin_under']
        bet12_last_over = item['bet12_last_over']
        bet12_last_goal_handicap = item['bet12_last_goal_handicap']
        bet12_last_under = item['bet12_last_under']
        liji_origin_over = item['liji_origin_over']
        liji_origin_goal_handicap = item['liji_origin_goal_handicap']
        liji_origin_under = item['liji_origin_under']
        liji_last_over = item['liji_last_over']
        liji_last_goal_handicap = item['liji_last_goal_handicap']
        liji_last_under = item['liji_last_under']
        yinghe_origin_over = item['yinghe_origin_over']
        yinghe_origin_goal_handicap = item['yinghe_origin_goal_handicap']
        yinghe_origin_under = item['yinghe_origin_under']
        yinghe_last_over = item['yinghe_last_over']
        yinghe_last_goal_handicap = item['yinghe_last_goal_handicap']
        yinghe_last_under = item['yinghe_last_under']
        # bet18_origin_over = item['bet18_origin_over']
        # bet18_origin_goal_handicap = item['bet18_origin_goal_handicap']
        # bet18_origin_under = item['bet18_origin_under']
        # bet18_last_over = item['bet18_last_over']
        # bet18_last_goal_handicap = item['bet18_last_goal_handicap']
        # bet18_last_under = item['bet18_last_under']
        ladbrokes_origin_over = item['ladbrokes_origin_over']
        ladbrokes_origin_goal_handicap = item['ladbrokes_origin_goal_handicap']
        ladbrokes_origin_under = item['ladbrokes_origin_under']
        ladbrokes_last_over = item['ladbrokes_last_over']
        ladbrokes_last_goal_handicap = item['ladbrokes_last_goal_handicap']
        ladbrokes_last_under = item['ladbrokes_last_under']

        db_name = 'ds_analysis'
        self.db = self.mongo_client[db_name]  # 获得数据库的句柄
        col_name = 'over_under_info'
        self.coll = self.db[col_name]  # 获得collection的句柄
        updateItem = dict(
            bet365_origin_over=bet365_origin_over,
            bet365_origin_goal_handicap=bet365_origin_goal_handicap,
            bet365_origin_under=bet365_origin_under,
            bet365_last_over=bet365_last_over,
            bet365_last_goal_handicap=bet365_last_goal_handicap,
            bet365_last_under=bet365_last_under,
            # Crown_origin_over=Crown_origin_over,
            # Crown_origin_goal_handicap=Crown_origin_goal_handicap,
            # Crown_origin_under=Crown_origin_under,
            # Crown_last_over=Crown_last_over,
            # Crown_last_goal_handicap=Crown_last_goal_handicap,
            # Crown_last_under=Crown_last_under,
            yishengbo_origin_over=yishengbo_origin_over,
            yishengbo_origin_goal_handicap=yishengbo_origin_goal_handicap,
            yishengbo_origin_under=yishengbo_origin_under,
            yishengbo_last_over=yishengbo_last_over,
            yishengbo_last_goal_handicap=yishengbo_last_goal_handicap,
            yishengbo_last_under=yishengbo_last_under,
            weide_origin_over=weide_origin_over,
            weide_origin_goal_handicap=weide_origin_goal_handicap,
            weide_origin_under=weide_origin_under,
            weide_last_over=weide_last_over,
            weide_last_goal_handicap=weide_last_goal_handicap,
            weide_last_under=weide_last_under,
            mingsheng_origin_over=mingsheng_origin_over,
            mingsheng_origin_goal_handicap=mingsheng_origin_goal_handicap,
            mingsheng_origin_under=mingsheng_origin_under,
            mingsheng_last_over=mingsheng_last_over,
            mingsheng_last_goal_handicap=mingsheng_last_goal_handicap,
            mingsheng_last_under=mingsheng_last_under,
            bet10_origin_over=bet10_origin_over,
            bet10_origin_goal_handicap=bet10_origin_goal_handicap,
            bet10_origin_under=bet10_origin_under,
            bet10_last_over=bet10_last_over,
            bet10_last_goal_handicap=bet10_last_goal_handicap,
            bet10_last_under=bet10_last_under,
            jinbaobo_origin_over=jinbaobo_origin_over,
            jinbaobo_origin_goal_handicap=jinbaobo_origin_goal_handicap,
            jinbaobo_origin_under=jinbaobo_origin_under,
            jinbaobo_last_over=jinbaobo_last_over,
            jinbaobo_last_goal_handicap=jinbaobo_last_goal_handicap,
            jinbaobo_last_under=jinbaobo_last_under,
            bet12_origin_over=bet12_origin_over,
            bet12_origin_goal_handicap=bet12_origin_goal_handicap,
            bet12_origin_under=bet12_origin_under,
            bet12_last_over=bet12_last_over,
            bet12_last_goal_handicap=bet12_last_goal_handicap,
            bet12_last_under=bet12_last_under,
            liji_origin_over=liji_origin_over,
            liji_origin_goal_handicap=liji_origin_goal_handicap,
            liji_origin_under=liji_origin_under,
            liji_last_over=liji_last_over,
            liji_last_goal_handicap=liji_last_goal_handicap,
            liji_last_under=liji_last_under,
            yinghe_origin_over=yinghe_origin_over,
            yinghe_origin_goal_handicap=yinghe_origin_goal_handicap,
            yinghe_origin_under=yinghe_origin_under,
            yinghe_last_over=yinghe_last_over,
            yinghe_last_goal_handicap=yinghe_last_goal_handicap,
            yinghe_last_under=yinghe_last_under,
            # bet18_origin_over=bet18_origin_over,
            # bet18_origin_goal_handicap=bet18_origin_goal_handicap,
            # bet18_origin_under=bet18_origin_under,
            # bet18_last_over=bet18_last_over,
            # bet18_last_goal_handicap=bet18_last_goal_handicap,
            # bet18_last_under=bet18_last_under,
            ladbrokes_origin_over=ladbrokes_origin_over,
            ladbrokes_origin_goal_handicap=ladbrokes_origin_goal_handicap,
            ladbrokes_origin_under=ladbrokes_origin_under,
            ladbrokes_last_over=ladbrokes_last_over,
            ladbrokes_last_goal_handicap=ladbrokes_last_goal_handicap,
            ladbrokes_last_under=ladbrokes_last_under,
        )
        try:
            if self.coll.find({'match_id': match_id}).count() != 0:
                if not 'bet365_origin_over' in self.coll.find_one({'match_id': match_id}):
                    self.coll.update({"match_id": match_id},
                                         {'$set': updateItem})
            # else:
            #     self.coll.update({"match_id": match_id},
            #                      {'$inc': {'home_shemen': home_shemen, 'away_shemen': away_shemen,
            #                                'home_shezheng': home_shezheng, 'away_shezheng': away_shezheng,
            #                                'home_attack': home_attack, 'away_attack': away_attack,
            #                                'home_danger': home_danger, 'away_danger': away_danger,
            #                                }})
        except Exception as err:
            print('%s\n%s' % (err, traceback.format_exc()))
        finally:
            self.mongo_client.close()
        return item
