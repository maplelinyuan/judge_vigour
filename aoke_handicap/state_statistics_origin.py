import pdb, traceback
from pymongo import MongoClient
import time
import redis
import json
import matplotlib.pyplot as plt

mongo_client = MongoClient(host='localhost', port=27019)
db_name = 'aoke_handicap'
db = mongo_client[db_name]  # 获得数据库的句柄
col_name = 'judge_vigour'
coll = db[col_name]  # 获得collection的句柄

total_point = 0
total_right = 0
total_num = 0

prev_is_false_count = 0
index_arr = []
total_point_arr = []

inc = 0
choose_inc = 0
for item in coll.find({'league_name': '美职'}):
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
    if abs(vigour_difference) >= 0.5:
        if vigour_difference < 0:
            if handicap_result > 0.25:
                total_point += (handicap_home_odd-1)
                total_right += 1
                prev_is_false_count = 0
            elif handicap_result > 0:
                total_point += (handicap_home_odd-1)/2
                total_right += 1
                prev_is_false_count = 0
            elif handicap_result == 0:
                total_right += 1
                prev_is_false_count = 0
                pass
            elif handicap_result >= -0.25:
                total_point -= 0.5
                prev_is_false_count += 1
                if (prev_is_false_count > 2): print('报警')
            else:
                total_point -= 1
                prev_is_false_count += 1
                if (prev_is_false_count > 2): print('报警')
            total_num += 1
        else:
            if handicap_result < -0.25:
                total_point += (handicap_away_odd-1)
                total_right += 1
                prev_is_false_count = 0
            elif handicap_result < 0:
                total_point += (handicap_away_odd-1)/2
                total_right += 1
                prev_is_false_count = 0
            elif handicap_result == 0:
                total_right += 1
                prev_is_false_count = 0
                pass
            elif handicap_result <= 0.25:
                total_point -= 0.5
                prev_is_false_count += 1
                if (prev_is_false_count > 2): print('报警')
            else:
                total_point -= 1
                prev_is_false_count += 1
                if (prev_is_false_count > 2): print('报警')
            total_num += 1
        choose_inc += 1
    index_arr.append(inc)
    total_point_arr.append(total_point/(choose_inc+1))
    inc += 1
plt.plot(index_arr, total_point_arr)
plt.show()


print("总分是%s, 比率是%s, 赢盘走盘数: %s, 比例是: %s" % (total_point, total_point/total_num, total_right, total_right/total_num));