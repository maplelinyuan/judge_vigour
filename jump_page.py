from selenium import webdriver
# from bs4 import BeautifulSoup
import pdb, traceback
from pymongo import MongoClient
import os
import redis

# 需要修改的url链接
give_me_url = 'http://zq.win007.com/cn/League/2015-2016/36.html'

try:
    mongo_client = MongoClient(host='localhost', port=27019)
    r = redis.Redis(host='localhost', port=6381, db=0)
    db_name = 'ds_analysis'
    db = mongo_client[db_name]  # 获得数据库的句柄
    col_name = 'over_under_info'
    coll = db[col_name]  # 获得collection的句柄

    driver = webdriver.Chrome()
    driver.get(give_me_url)
    driver.implicitly_wait(10)

    league_name = driver.find_elements_by_xpath('//a[@style="color:red"]')[0].text
    end_find_count = 3      # 小于1就提前结束
    for elem in driver.find_elements_by_xpath('//td[@class="lsm2"]'):
        if end_find_count < 1:
            break
        print(elem.text)
        elem.click()
        for single_match in driver.find_elements_by_xpath('//table[@id="Table3"]/tbody/tr[@align="center"]'):
            home_name = single_match.find_elements_by_xpath('td')[2].find_elements_by_xpath('a')[0].text
            away_name = single_match.find_elements_by_xpath('td')[4].find_elements_by_xpath('a')[0].text
            score = single_match.find_elements_by_xpath('td')[3].find_elements_by_xpath('div/a/strong')[0].text
            start_time = single_match.find_elements_by_xpath('td')[1].text.replace('\n', ' ')
            if score == '':
                end_find_count -= 1
                continue
            home_goal = int(score.split('-')[0])
            away_goal = int(score.split('-')[1])
            if home_goal > away_goal:
                result = 3
            elif home_goal == away_goal:
                result = 1
            else:
                result = 0
            if home_goal + away_goal > 2:
                big_goal = 1
            else:
                big_goal = 0
            get_href = single_match.find_elements_by_xpath('td')[9].find_elements_by_xpath('a')[3].get_attribute('href')
            match_id = get_href.split('=')[-1]
            insertItem = dict(match_id=match_id,
                              home_name=home_name,
                              away_name=away_name,
                              league_name=league_name,
                              start_time=start_time,
                              result=result,
                              big_goal=big_goal)
            if coll.find({'match_id': match_id}).count() == 0:
                coll.insert(insertItem)
                r.lpush('qiutan_analysis:start_urls', get_href)

except Exception as err:
    print('%s\n%s' % (err, traceback.format_exc()))
finally:
    mongo_client.close()



