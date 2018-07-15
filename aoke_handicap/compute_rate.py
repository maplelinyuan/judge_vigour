import pdb, traceback
from pymongo import MongoClient
import time
import redis
import json

mongo_client = MongoClient(host='localhost', port=27019)
db_name = 'aoke_handicap'
db = mongo_client[db_name]  # 获得数据库的句柄
col_name = 'change_analysis'
coll = db[col_name]  # 获得collection的句柄

total_point = 0
total_right = 0
total_num = 0

for item in coll.find({'league_name': 'J2联赛'}):
    match_id = item['match_id']
    home_goal = item['home_goal']
    away_goal = item['away_goal']
    handicap_num = item['handicap_num']
    support_direction = item['support_direction']
    goal_difference = home_goal - away_goal - handicap_num
    if goal_difference > 0:
        if goal_difference > 0.25:
            if support_direction == 0:
                total_point += 1
                total_right += 1
            else:
                total_point -= 1
        else:
            if support_direction == 0:
                total_point += 0.5
                total_right += 1
            else:
                total_point -= 0.5
    elif goal_difference < 0:
        if goal_difference < -0.25:
            if support_direction == 1:
                total_point += 1
                total_right += 1
            else:
                total_point -= 1
        else:
            if support_direction == 1:
                total_point += 0.5
                total_right += 0.5
            else:
                total_point -= 0.5
    total_num += 1
print("总分是%s, 比率是%s, 总正确数: %s, 比例是: %s" % (total_point, total_point/total_num, total_right, total_right/total_num));