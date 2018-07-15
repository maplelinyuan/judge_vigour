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
give_me_url = 'http://www.okooo.com/soccer/league/17/schedule/13222/'

try:
    mongo_client = MongoClient(host='localhost', port=27019)
    db_name = 'aoke_handicap'
    db = mongo_client[db_name]  # 获得数据库的句柄
    col_name = 'handicap_changes'
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
    driver.implicitly_wait(20)
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

            # 根据联赛修改Limit_time, 五大联赛为200*60，其他为其一半
            js = """
                // 使用利记亚盘页面
                // 变化限制时间180min
                // 最小截至时间8hour, 最大截至时间48h
                // 临界概率变化0.03
                // 取截至时间前的最新值
                // support_direction：0为主队盘口，1为客队盘口
                
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
                    return handicap_name_dict[handicap_name]
                }
                
                function isInArray(arr,val){
                　　var testStr=','+arr.join(",")+",";
                　　return testStr.indexOf(","+val+",")!=-1;
                }
                
                limit_time = 180;
                min_time = 480;
                max_time = 2880;
                limit_pro = 0.02;
                result_arr = [];
                first_table = $('table').eq(0);
                // 先存储所有时间
                all_time_arr = [];
                first_table.find('tr:not(.titlebg)').each(function () {
                    var first_tr = $(this);
                    if (first_tr.find('td').length === 0){
                            return true
                    }
                    cur_hour = parseInt(first_tr.find('td').eq(1).text().split('赛前')[1].split('时')[0]);
                    cur_minute = parseInt(first_tr.find('td').eq(1).text().split('赛前')[1].split('时')[1].split('分')[0]);
                    cur_time = cur_hour * 60 + cur_minute;
                    all_time_arr.push(cur_time);
                });
                table_index = 0;
                $('.ahChangeTable').each(function(){
                    index = 0;
                    prev_home_pro = '-';
                    var table = $(this);
                    table.find('tr:not(.titlebg)').each(function(){
                        var tr = $(this);
                        if (tr.find('td').length === 0 || $.trim(tr.find('td').eq(0).text()) === '-'){
                            index += 1;
                            return true
                        }
                        if (first_table.find('tr:not(.titlebg)').eq(index).find('td').eq(1).text().split('赛前')[1] === undefined){
                            return true
                        }
                        cur_hour = parseInt(first_table.find('tr:not(.titlebg)').eq(index).find('td').eq(1).text().split('赛前')[1].split('时')[0]);
                        cur_minute = parseInt(first_table.find('tr:not(.titlebg)').eq(index).find('td').eq(1).text().split('赛前')[1].split('时')[1].split('分')[0]);
                        cur_time = (cur_hour*60+cur_minute);
                        need_analysis_time_arr = [];
                        // 去总时间数组中遍历得到小于当前时间，大于等于(当前时间-limit_time)的index
                        for(i = 0; i < all_time_arr.length; i++){
                            if (all_time_arr[i] < cur_time && all_time_arr[i] >= (cur_time-limit_time)){
                                need_analysis_time_arr.push(i)
                            }
                        }
                
                        cur_odd_home = parseFloat($.trim(tr.find('td').eq(0).text()));
                        cur_odd_away = parseFloat($.trim(tr.find('td').eq(1).text()));
                        return_rate = parseFloat((cur_odd_home*cur_odd_away/(cur_odd_home + cur_odd_away)).toFixed(3));
                        home_pro = parseFloat((return_rate/cur_odd_home) .toFixed(3));
                        cur_handicap_num = convert_handicap(($.trim(table.find('tr.tableh').eq(0).text())));
                        current_table_trs = $('.ahChangeTable').eq(table_index).find('tr:not(.titlebg)');
                        for(i = 0; i < need_analysis_time_arr.length; i++){
                            need_analysis_tr = current_table_trs.eq(need_analysis_time_arr[i] + 1);
                            need_analysis_odd_home = parseFloat($.trim(need_analysis_tr.find('td').eq(0).text()));
                            need_analysis_odd_away = parseFloat($.trim(need_analysis_tr.find('td').eq(1).text()));
                            need_analysis_return_rate = parseFloat((need_analysis_odd_home*need_analysis_odd_away/(need_analysis_odd_home + need_analysis_odd_away)).toFixed(3));
                            need_analysis_home_pro = parseFloat((need_analysis_return_rate/need_analysis_odd_home) .toFixed(3));
                            if (Math.abs(need_analysis_home_pro - home_pro) > limit_pro){
                                pro_change = parseFloat((need_analysis_home_pro - home_pro).toFixed(3));
                                if (pro_change > 0){
                                    cur_info = {
                                        'cur_time': cur_time,
                                        'last_time': all_time_arr[need_analysis_time_arr[i]],
                                        'cur_handicap_num': cur_handicap_num,
                                        'pro_change': pro_change,
                                        'support_direction': 0
                                    };
                                    result_times = [];
                                    for (j in result_arr){
                                        result_times.push(result_arr[j]['cur_time'])
                                    }
                                    if (all_time_arr[need_analysis_time_arr[i]] >= min_time && all_time_arr[need_analysis_time_arr[i]] <= max_time){
                                        if (result_times.length === 0){
                                            if (!isInArray(result_times, cur_time)){
                                                result_arr.push(cur_info)
                                            }
                                        } else {
                                            if (cur_time > result_times[0]){
                                                result_arr = [cur_info]
                                            }
                                        }
                                    }
                                } else {
                                    cur_info = {
                                        'cur_time': cur_time,
                                        'last_time': all_time_arr[need_analysis_time_arr[i]],
                                        'cur_handicap_num': cur_handicap_num,
                                        'pro_change': pro_change,
                                        'support_direction': 1
                                    };
                                    result_times = [];
                                    for (j in result_arr){
                                        result_times.push(result_arr[j]['cur_time'])
                                    }
                                    if (all_time_arr[need_analysis_time_arr[i]] >= min_time && all_time_arr[need_analysis_time_arr[i]] <= max_time) {
                                        if (result_times.length === 0) {
                                            if (!isInArray(result_times, cur_time)) {
                                                result_arr.push(cur_info)
                                            }
                                        } else {
                                            if (cur_time > result_times[0]) {
                                                result_arr = [cur_info]
                                            }
                                        }
                                    }
                                }
                            }
                        }
                        index += 1
                    });
                    table_index += 1
                });
                return result_arr[0];

                """
            try:
                liji_tr = WebDriverWait(driver, 15).until(lambda driver: driver.find_element_by_id("tr280"))
                liji_tr.find_elements_by_xpath('td')[6].find_elements_by_xpath('a')[0].find_elements_by_xpath('span')[
                    0].click()
                windows = driver.window_handles
                driver.switch_to.window(windows[-1])
                current_handicap_dict = driver.execute_script(js)
                print(current_handicap_dict)
                if not current_handicap_dict == None:
                    insertItem = dict(
                        match_id=match_id,
                        league_name=league_name,
                        home_name=home_name,
                        away_name=away_name,
                        home_goal=home_goal,
                        away_goal=away_goal,
                        liji_cur_handicap_num=current_handicap_dict['cur_handicap_num'],
                        liji_pro_change=current_handicap_dict['pro_change'],
                        liji_support_direction=current_handicap_dict['support_direction'],
                    )
                    if coll.find({'match_id': match_id}).count() == 0:
                        coll.insert(insertItem)
                windows = driver.window_handles
                driver.switch_to.window(windows[-1])
                driver.close()
            except Exception as err:
                print('%s\n%s' % (err, traceback.format_exc()))
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



