# -*- coding:utf-8 -*-
from selenium import webdriver
# from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from PIL import Image,ImageEnhance
import pytesseract
import pdb, traceback
from pymongo import MongoClient
import os
import time
import redis
import json

def get_auth_code(driver, codeEelement):
    '''获取验证码'''
    driver.save_screenshot('login/login.png')  #截取登录页面
    imgSize = codeEelement.size   #获取验证码图片的大小
    imgLocation = codeEelement.location #获取验证码元素坐标
    rangle = (int(imgLocation['x']),int(imgLocation['y']),int(imgLocation['x'] + imgSize['width']),int(imgLocation['y']+imgSize['height']))  #计算验证码整体坐标
    login = Image.open("login/login.png")
    frame4 = login.crop(rangle)   #截取验证码图片
    frame4.save('login/authcode.png')
    authcodeImg = Image.open('login/authcode.png')
    authCodeText = pytesseract.image_to_string(authcodeImg).strip()
    return authCodeText

# 需要修改的url链接
give_me_url = 'http://www.okooo.com/soccer/league/402/schedule/13047/1/'

try:
    mongo_client = MongoClient(host='localhost', port=27019)
    r = redis.Redis(host='localhost', port=6381, db=0)
    db_name = 'aoke_handicap'
    db = mongo_client[db_name]  # 获得数据库的句柄
    col_name = 'change_analysis'
    coll = db[col_name]  # 获得collection的句柄

    service_args = []
    service_args.append('--load-images=no')
    service_args.append('--dick-cache=yes')
    service_args.append('--ignore-ssl-errors=true')
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    driver = webdriver.Chrome(chrome_options=chrome_options, desired_capabilities=dcap, service_args=service_args)
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(30)
    driver.get(give_me_url)

    # 删除第一次建立连接时的cookie
    # driver.delete_all_cookies()
    # 读取登录时存储到本地的cookie
    with open('cookies.json', 'r', encoding='utf-8') as f:
        listCookies = json.loads(f.read())
    for cookie in listCookies:
        driver.add_cookie({
            'domain': 'http://www.okooo.com',  # 此处xxx.com前，需要带点
            'name': cookie['name'],
            'value': cookie['value'],
            'path': '/',
            'expires': None
        })

    league_name = driver.find_elements_by_xpath('//div[@class="LotteryListTitle"]')[0].text     # 联赛名称

    end_find_count = 3  # 小于1就提前结束
    first_click = True
    match_day_total = len(driver.find_elements_by_xpath('//td[@class="linkblock"]'))
    for match_day_index in range(0, match_day_total):
        if end_find_count < 1:
            break
        if not first_click:
            match_day_index -= 1
        first_click = False
        windows = driver.window_handles
        driver.switch_to.window(windows[0])
        # print(elem.text)
        driver.find_elements_by_xpath('//td[@class="linkblock"]')[match_day_index].click()
        for single_match in driver.find_elements_by_xpath('//table[@id="team_fight_table"]/tbody/tr[@align="center"]'):
            if single_match.get_attribute('class') == 'LotteryListTitle' or len(single_match.find_elements_by_xpath('td')[3].find_elements_by_xpath('a')) == 0:
                continue
            match_id = single_match.get_attribute('matchid')
            home_name = single_match.find_elements_by_xpath('td')[2].text
            away_name = single_match.find_elements_by_xpath('td')[4].text
            score = single_match.find_elements_by_xpath('td')[3].find_elements_by_xpath('a')[0].find_elements_by_xpath('strong')[0].text
            home_goal = int(score.split('-')[0])
            away_goal = int(score.split('-')[1])

            single_match.find_elements_by_xpath('td')[-1].find_elements_by_xpath('a')[1].click()
            windows = driver.window_handles
            driver.switch_to.window(windows[-1])
            driver.find_elements_by_xpath('//div[@id="qnav"]/div')[0].find_elements_by_xpath('a')[1].find_elements_by_xpath('p')[0].click()

            time.sleep(3)
            login_window = driver.find_elements_by_xpath('//div[@id="login_bg"]')[0]
            if login_window.is_displayed():
                print('需要登录！')
                # 方案1，识别验证码，成功率较低
                # user_id_input = login_window.find_elements_by_xpath('div[@class="loginbox_login"]')[0].find_elements_by_xpath('ul[@id="head_login_info"]')[0].find_elements_by_xpath('li')[0].find_elements_by_xpath('input[@id="login_name"]')[0]
                # password_input = login_window.find_elements_by_xpath('div[@class="loginbox_login"]')[0].find_elements_by_xpath('ul[@id="head_login_info"]')[0].find_elements_by_xpath('li')[1].find_elements_by_xpath('input[@id="login_pwd"]')[0]
                # auth_input = login_window.find_elements_by_xpath('div[@class="loginbox_login"]')[0].find_elements_by_xpath('ul[@id="head_login_info"]')[0].find_elements_by_xpath('li')[2].find_elements_by_xpath('dl')[0].find_elements_by_xpath('dd')[0].find_elements_by_xpath('input[@id="AuthCode"]')[0]
                # authcode_img = login_window.find_elements_by_xpath('div[@class="loginbox_login"]')[0].find_elements_by_xpath('ul[@id="head_login_info"]')[0].find_elements_by_xpath('li')[2].find_elements_by_xpath('dl')[0].find_elements_by_xpath('dd')[1].find_elements_by_xpath('p')[0].find_elements_by_xpath('img[@id="randomNoImg"]')[0]
                # login_button = login_window.find_elements_by_xpath('div[@class="loginbox_login"]')[0].find_elements_by_xpath('ul[@id="head_login_info"]')[0].find_elements_by_xpath('li')[5].find_elements_by_xpath('input[@id="LoginSubmit"]')[0]
                # auth_coe = get_auth_code(driver, authcode_img)
                login_window.find_elements_by_xpath('div[@class="mfzc"]')[0].find_elements_by_xpath('p')[1].find_elements_by_xpath('a')[0].click()
                windows = driver.window_handles
                driver.switch_to.window(windows[-1])
                driver.switch_to.frame("ptlogin_iframe")        # 跳入frame
                driver.find_elements_by_xpath('//span[@id="img_out_1015143338"]')[0].click()
                driver.switch_to.default_content()      # 跳出frame
                windows = driver.window_handles
                driver.switch_to.window(windows[-1])
                # 获取cookie并通过json模块将dict转化成str
                dictCookies = driver.get_cookies()
                jsonCookies = json.dumps(dictCookies)
                # 登录完成后，将cookie保存到本地文件
                with open('cookies.json', 'w') as f:
                    f.write(jsonCookies)
            else:
                print('已经登录')

            bet365_tr = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id("tr27"))
            bet365_tr.find_elements_by_xpath('td')[6].find_elements_by_xpath('a')[0].find_elements_by_xpath('span')[0].click()
            windows = driver.window_handles
            driver.switch_to.window(windows[-1])
            # 根据联赛修改Limit_time, 五大联赛为200*60，其他为其一半
            js = """
                limit_time = 100 * 60
                function convert_handicap(handicap_name) {
                    handicap_name_dict = {
                        '受三球': -3,
                        '受两球半/三球': -2.75,
                        '受两球半': -2.5,
                        '受两球/两球半': -2.25,
                        '受两球': -2,
                        '受球半/两球': -1.75,
                        '受球半': -1.5,
                        '受一球/球半': -1.25,
                        '受一球': -1,
                        '受半球/一球': -0.75,
                        '受半球': -0.5,
                        '受平手/半球': -0.25,
                        '平手': 0,
                        '平手/半球': 0.25,
                        '半球': 0.5,
                        '半球/一球': 0.75,
                        '一球': 1,
                        '一球/球半': 1.25,
                        '球半': 1.5,
                        '球半/两球': 1.75,
                        '两球': 2,
                        '两球/两球半': 2.25,
                        '两球半': 2.5,
                        '两球半/三': 2.75,
                        '三球': 3,
                    };
                    return handicap_name_dict[handicap_name];
                };
                
                result_dict = {'latest_minute': 999999};
                $('.ahChangeTable').each(function(){
                    index = 0;
                    prev_odd = '-';
                    var table = $(this);
                    table.find('tr:not(.titlebg)').each(function(){
                        var tr = $(this);
                        if (tr.find('td').length === 0){
                            return true;
                        }
                        cur_odd = parseFloat($.trim($(this).find('td').eq(0).text()));
                        if (prev_odd !== '-' && cur_odd < 2.15){
                            if (Math.abs(cur_odd - prev_odd) > 0.091){
                                cur_hour = parseInt($('table').eq(0).find('tr').eq(index+2).find('td').eq(1).text().split('赛前')[1].split('时')[0]);
                                pre_hour = parseInt($('table').eq(0).find('tr').eq(index+1).find('td').eq(1).text().split('赛前')[1].split('时')[0]);
                                cur_minute = parseInt($('table').eq(0).find('tr').eq(index+2).find('td').eq(1).text().split('赛前')[1].split('时')[1].split('分')[0]);
                                pre_minute = parseInt($('table').eq(0).find('tr').eq(index+1).find('td').eq(1).text().split('赛前')[1].split('时')[1].split('分')[0]);
                                total_minute_difference = (cur_hour*60+cur_minute) - (pre_hour*60+pre_minute);
                                if (0 < total_minute_difference && total_minute_difference <= 120 && pre_hour*60+pre_minute > 2 && pre_hour*60+pre_minute < limit_time){
                                    if (cur_odd > prev_odd){
                                        support_direction = 0;
                                    } else {
                                        support_direction = 1;
                                    }
                                    if (pre_hour*60+pre_minute <= result_dict['latest_minute']){
                                        if (support_direction === 0){
                                            // 如果支持方向是主队，如果盘口更大，则保存，否则跳过
                                            handicap_num = convert_handicap(table.find('tr').eq(0).find('th').text());		// 盘口大小
                                            if (typeof result_dict['handicap_num'] === 'undefined' || handicap_num > result_dict['handicap_num']){
                                                result_dict['support_direction'] = support_direction;
                                                result_dict['handicap_num'] = handicap_num;
                                                result_dict['latest_minute'] = pre_hour*60+pre_minute;
                                            }
                                        } else {
                                            // 如果支持方向是客队，如果盘口更小，则保存，否则跳过
                                            handicap_num = convert_handicap(table.find('tr').eq(0).find('th').text());		// 盘口大小
                                            if (typeof result_dict['handicap_num'] === 'undefined' || handicap_num < result_dict['handicap_num']){
                                                result_dict['support_direction'] = support_direction;
                                                result_dict['handicap_num'] = handicap_num;
                                                result_dict['latest_minute'] = pre_hour*60+pre_minute;
                                            }
                                        }
                                    }
                                }
                            }
                        }
                        prev_odd = cur_odd;
                        index += 1;
                    });
                });
                return result_dict;
                """
            support_result = driver.execute_script(js)
            print(support_result)
            if support_result['latest_minute'] != 999999:
                insertItem = dict(match_id=match_id,
                                  league_name=league_name,
                                  home_name=home_name,
                                  away_name=away_name,
                                  home_goal=home_goal,
                                  away_goal=away_goal,
                                  handicap_num=support_result['handicap_num'],
                                  latest_minute=support_result['latest_minute'],
                                  support_direction=support_result['support_direction'],
                                  )
                if coll.find({'match_id': match_id}).count() == 0:
                    coll.insert(insertItem)
            driver.close()
            windows = driver.window_handles
            driver.switch_to.window(windows[-1])
            driver.close()
            driver.switch_to.window(windows[0])

    # 关闭窗口
    driver.quit()

except Exception as err:
    print('%s\n%s' % (err, traceback.format_exc()))
finally:
    mongo_client.close()



