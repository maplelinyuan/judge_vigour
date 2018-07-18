import pdb, traceback
from pymongo import MongoClient
import time
import redis
import json

mongo_client = MongoClient(host='localhost', port=27019)
db_name = 'aoke_handicap'
db = mongo_client[db_name]  # 获得数据库的句柄
col_name = 'judge_vigour'
coll = db[col_name]  # 获得collection的句柄

total_point = 0
total_right = 0
total_num = 0

for item in coll.find({'league_name': '美公开杯'}):
# for item in coll.find():
    match_id = item['match_id']
    home_name = item['home_name']
    away_name = item['away_name']
    home_goal = item['home_goal']
    away_goal = item['away_goal']
    this_match_handicap_num = item['this_match_handicap_num']
    handicap_home_odd = item['handicap_home_odd']
    handicap_away_odd = item['handicap_away_odd']
    vigour_difference = item['vigour_difference']

    handicap_result = home_goal - away_goal - this_match_handicap_num
    if abs(vigour_difference) >= 0.35:
        if vigour_difference > 0:
            if handicap_result > 0.25:
                total_point += (handicap_home_odd-1)
                total_right += 1
            elif handicap_result > 0:
                total_point += (handicap_home_odd-1)/2
                total_right += 1
            elif handicap_result == 0:
                total_right += 1
                pass
            elif handicap_result >= -0.25:
                total_point -= 0.5
            else:
                total_point -= 1
            total_num += 1
        else:
            if handicap_result < -0.25:
                total_point += (handicap_away_odd-1)
                total_right += 1
            elif handicap_result < 0:
                total_point += (handicap_away_odd-1)/2
                total_right += 1
            elif handicap_result == 0:
                total_right += 1
                pass
            elif handicap_result <= 0.25:
                total_point -= 0.5
            else:
                total_point -= 1
            total_num += 1

print("总分是%s, 比率是%s, 赢盘走盘数: %s, 比例是: %s" % (total_point, total_point/total_num, total_right, total_right/total_num));