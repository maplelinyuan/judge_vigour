import pdb, traceback
from pymongo import MongoClient
import time
import redis
import json

mongo_client = MongoClient(host='localhost', port=27019)
db_name = 'aoke_handicap'
db = mongo_client[db_name]  # 获得数据库的句柄
col_name = 'handicap_changes'
coll = db[col_name]  # 获得collection的句柄

total_point = 0
total_right = 0
total_num = 0

for item in coll.find({'league_name': '英超'}):
# for item in coll.find():
    match_id = item['match_id']
    home_goal = item['home_goal']
    away_goal = item['away_goal']
    liji_cur_handicap_num = item['liji_cur_handicap_num']
    liji_support_direction = item['liji_support_direction']

    handicap_result = home_goal - away_goal - liji_cur_handicap_num
    if liji_support_direction == 0:
        if handicap_result > 0.25:
            total_point += 1
            total_right += 1
        elif handicap_result > 0:
            total_point += 0.5
            total_right += 1
        elif handicap_result == 0:
            pass
        else:
            total_point -= 1
        total_num += 1
    elif liji_support_direction == 1:
        if handicap_result < -0.25:
            total_point += 1
            total_right += 1
        elif handicap_result < 0:
            total_point += 0.5
            total_right += 1
        elif handicap_result == 0:
            pass
        else:
            total_point -= 1
        total_num += 1


print("总分是%s, 比率是%s, 总正确数: %s, 比例是: %s" % (total_point, total_point/total_num, total_right, total_right/total_num));