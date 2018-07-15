from pymongo import MongoClient
import datetime, time
import pdb
import traceback

mongo_client = MongoClient(host='localhost', port=27019)
try:
    # self.mongo_client.admin.authenticate(settings['MINGO_USER'], settings['MONGO_PSW'])     #如果有账户密码
    db_name = 'ds_analysis'
    db = mongo_client[db_name]  # 获得数据库的句柄
    col_name = 'battle_info'
    coll = db[col_name]  # 获得collection的句柄

    for item in coll.find({'net_goal': {'$exists': False}}):
        match_id = item['match_id']
        home_point = item['home_point']
        away_point = item['away_point']
        if home_point >= away_point:
            if away_point == 0:
                away_point = 0.1
            home_expect_goal = round(home_point/away_point, 2)
            away_expect_goal = 1
            net_goal = round(home_expect_goal - 1, 2)
        else:
            if home_point == 0:
                home_point = 0.1
            away_expect_goal = round(away_point / home_point, 2)
            home_expect_goal = 1
            net_goal = round(1 - away_expect_goal, 2)
        coll.update({"match_id": match_id},
                         {'$set': {'home_expect_goal': home_expect_goal, 'away_expect_goal': away_expect_goal, 'net_goal': net_goal}})
except Exception as err:
    print('%s\n%s' % (err, traceback.format_exc()))
finally:
    mongo_client.close()