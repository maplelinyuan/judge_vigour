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

def convert_handicap(handicap_name) :
    handicap_name_dict = {
        '受三球半': -3.5,
        '受三球/三球半': -3.25,
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
        '两球半/三球': 2.75,
        '三球': 3,
        '三球/三球半': 3.25,
        '三球半': 3.5,
        '三球半/四球': 3.75,
        '四球': 4,
        '四球/四球半': 4.25,
        '四球半': 4.5,
    }
    return handicap_name_dict[handicap_name]

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
give_me_url = 'http://www.okooo.com/soccer/league/615/schedule/13756/'

try:
    mongo_client = MongoClient(host='localhost', port=27019)
    db_name = 'aoke_handicap'
    db = mongo_client[db_name]  # 获得数据库的句柄
    col_name = 'judge_vigour'
    coll = db[col_name]  # 获得collection的句柄

    service_args = []
    service_args.append('--load-images=no')
    service_args.append('--dick-cache=yes')
    service_args.append('--ignore-ssl-errors=true')
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
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

    group_total = len(driver.find_elements_by_xpath('//div[@class="ButtonBg04_Off"]')) + 1
    group_first_click = True
    for group_index in range(0, group_total):
        if not group_first_click:
            group_index -= 1
        group_first_click = False
        # 如果存在分组则点击
        if group_total != 1:
            driver.find_elements_by_xpath('//div[@class="ButtonBg04_Off"]')[group_index].find_elements_by_xpath('a')[0].click()

        first_click = True
        match_day_total = len(driver.find_elements_by_xpath('//td[@class="linkblock"]')) + 1
        for match_day_index in range(0, match_day_total):
            if not first_click:
                match_day_index -= 1
            first_click = False
            windows = driver.window_handles
            driver.switch_to.window(windows[0])
            # print(elem.text)
            # 美职联当前赛季没有linkblock
            if match_day_total != 1:
                driver.find_elements_by_xpath('//td[@class="linkblock"]')[match_day_index].click()
            for single_match in driver.find_elements_by_xpath('//table[@id="team_fight_table"]/tbody/tr[@align="center"]'):
                match_id = single_match.get_attribute('matchid')
                if single_match.get_attribute('class') == 'LotteryListTitle' or coll.find({'match_id': match_id}).count() > 0:
                    continue
                if len(single_match.find_elements_by_xpath('td')[3].find_elements_by_xpath('a')) == 0:
                    continue
                home_name = single_match.find_elements_by_xpath('td')[2].text
                away_name = single_match.find_elements_by_xpath('td')[4].text
                score = single_match.find_elements_by_xpath('td')[3].find_elements_by_xpath('a')[0].find_elements_by_xpath('strong')[0].text
                home_goal = int(score.split('-')[0])
                away_goal = int(score.split('-')[1])

                single_match.find_elements_by_xpath('td')[-1].find_elements_by_xpath('a')[1].click()
                windows = driver.window_handles
                driver.switch_to.window(windows[-1])
                # 进入详情页面
                this_match_handicap = WebDriverWait(driver, 30).until(lambda driver: driver.find_elements_by_xpath('//tr[@class="topjfbg jsThisMatch"]')[0])
                if len(this_match_handicap.find_elements_by_xpath('td')) < 11:
                    driver.close()
                    windows = driver.window_handles
                    driver.switch_to.window(windows[0])
                    continue
                this_match_handicap_text = this_match_handicap.find_elements_by_xpath('td')[10].get_attribute('textContent')
                if this_match_handicap_text == '-' or this_match_handicap_text == '':
                    driver.close()
                    windows = driver.window_handles
                    driver.switch_to.window(windows[0])
                    continue
                this_match_handicap_num = convert_handicap(this_match_handicap_text)
                this_match_handicap_home_odd_td = this_match_handicap.find_elements_by_xpath('td')[9]
                this_match_handicap_away_odd_td = this_match_handicap.find_elements_by_xpath('td')[11]
                if len(this_match_handicap_home_odd_td.find_elements_by_xpath('span')) > 0:
                    handicap_home_odd = float(this_match_handicap_home_odd_td.find_elements_by_xpath('span')[0].get_attribute('textContent'))
                else:
                    handicap_home_odd = float(this_match_handicap_home_odd_td.get_attribute('textContent'))
                if len(this_match_handicap_away_odd_td.find_elements_by_xpath('span')) > 0:
                    handicap_away_odd = float(this_match_handicap_away_odd_td.find_elements_by_xpath('span')[0].get_attribute('textContent'))
                else:
                    handicap_away_odd = float(this_match_handicap_away_odd_td.get_attribute('textContent'))

                # 登录模块
                # time.sleep(3)
                # login_window = driver.find_elements_by_xpath('//div[@id="login_bg"]')[0]
                # if login_window.is_displayed():
                #     print('需要登录！')
                #     # 方案1，识别验证码，成功率较低
                #     # user_id_input = login_window.find_elements_by_xpath('div[@class="loginbox_login"]')[0].find_elements_by_xpath('ul[@id="head_login_info"]')[0].find_elements_by_xpath('li')[0].find_elements_by_xpath('input[@id="login_name"]')[0]
                #     # password_input = login_window.find_elements_by_xpath('div[@class="loginbox_login"]')[0].find_elements_by_xpath('ul[@id="head_login_info"]')[0].find_elements_by_xpath('li')[1].find_elements_by_xpath('input[@id="login_pwd"]')[0]
                #     # auth_input = login_window.find_elements_by_xpath('div[@class="loginbox_login"]')[0].find_elements_by_xpath('ul[@id="head_login_info"]')[0].find_elements_by_xpath('li')[2].find_elements_by_xpath('dl')[0].find_elements_by_xpath('dd')[0].find_elements_by_xpath('input[@id="AuthCode"]')[0]
                #     # authcode_img = login_window.find_elements_by_xpath('div[@class="loginbox_login"]')[0].find_elements_by_xpath('ul[@id="head_login_info"]')[0].find_elements_by_xpath('li')[2].find_elements_by_xpath('dl')[0].find_elements_by_xpath('dd')[1].find_elements_by_xpath('p')[0].find_elements_by_xpath('img[@id="randomNoImg"]')[0]
                #     # login_button = login_window.find_elements_by_xpath('div[@class="loginbox_login"]')[0].find_elements_by_xpath('ul[@id="head_login_info"]')[0].find_elements_by_xpath('li')[5].find_elements_by_xpath('input[@id="LoginSubmit"]')[0]
                #     # auth_coe = get_auth_code(driver, authcode_img)
                #     login_window.find_elements_by_xpath('div[@class="mfzc"]')[0].find_elements_by_xpath('p')[1].find_elements_by_xpath('a')[0].click()
                #     windows = driver.window_handles
                #     driver.switch_to.window(windows[-1])
                #     driver.switch_to.frame("ptlogin_iframe")        # 跳入frame
                #     driver.find_elements_by_xpath('//span[@id="img_out_1015143338"]')[0].click()
                #     driver.switch_to.default_content()      # 跳出frame
                #     windows = driver.window_handles
                #     driver.switch_to.window(windows[-1])
                #     # 获取cookie并通过json模块将dict转化成str
                #     dictCookies = driver.get_cookies()
                #     jsonCookies = json.dumps(dictCookies)
                #     # 登录完成后，将cookie保存到本地文件
                #     with open('cookies.json', 'w') as f:
                #         f.write(jsonCookies)
                # else:
                #     print('已经登录')

                # 根据联赛修改Limit_time, 五大联赛为200*60，其他为其一半
                js = """
                    limit_day = 15;     // 限制为limit_day天内的比赛
                    current_timestamp = new Date('20'+$('#lunci').next().find('p').eq(0).text().replace(/-/g,'/').replace(' ', " ")).getTime()/ 1000;
                    home_name = $('#matchTeam').find('.qb2_t_1').eq(0).find('div').eq(1).text();
                    away_name = $('#matchTeam').find('.qb2_t_1').eq(1).find('div').eq(0).text();
                    
                    // 返回返还率
                    function compute_returnrate(home_odd, draw_odd, away_odd){
                        return parseFloat((home_odd*draw_odd*away_odd/(home_odd*draw_odd + home_odd*away_odd + draw_odd*away_odd)).toFixed(3))
                    }
                    // 判断主队赛果
                    function home_match_result(home_Position, match_result){
                        if (match_result === 1){
                            return 1
                        } else {
                             if (home_Position === 0){
                                if (match_result === 3){
                                    return 3;
                                } else {
                                    return 0;
                                }
                            } else {
                                 if (match_result === 3){
                                    return 0;
                                } else {
                                    return 3;
                                }
                             }
                        }
                    }
                    
                    // 计算分数
                    function compute_vigour_change(position, result, home_pro, draw_pro, away_pro, goal_differ) {
                        var vigour = 0;
                        if (result === 3){
                            if (position === 0){
                                vigour -= draw_pro*(Math.log(goal_differ)+1);
                                vigour -= away_pro*(Math.log(goal_differ)+1);
                            } else{
                                 vigour -= home_pro*(Math.log(goal_differ)+1);
                                vigour -= draw_pro*(Math.log(goal_differ)+1);
                            }
                        } else if(result === 1){
                             if (position === 0){
                                vigour -= draw_pro/2;
                                vigour -= away_pro/2;
                            } else{
                                 vigour -= home_pro/2;
                                 vigour -= draw_pro/2;
                            }
                        } else{
                             if (position === 0){
                                vigour -= away_pro/(Math.log(goal_differ)+1);
                            } else{
                                vigour -= home_pro/(Math.log(goal_differ)+1);
                            }
                        }
                        return vigour
                    }
                    
                    // 最终的精力分数
                    home_vigour = 0;
                    away_vigour = 0;
                
                    is_latest_match = true;
                    $('.homecomp tr:not(:hidden)').each(function(){
                        cur_tr = $(this);
                        if (cur_tr.attr('class') === "titlebg" || cur_tr.attr('class') === "tableh"){
                            return true;
                        }
                        match_timestamp = new Date(cur_tr.find('td').eq(1).find('a').text().replace(/-/g,'/')).getTime()/ 1000;
                        if ((current_timestamp - match_timestamp) > limit_day*86400){
                            return true;
                        }
                        differ_day = (current_timestamp - match_timestamp)/86400;       // 距今几天
                        multi_num = Math.pow(1.1, -differ_day);        // 分数乘积
                        score = cur_tr.find('td').eq(3).text();
                        home_goal = parseInt(score.split('-')[0]);
                        away_goal = parseInt(score.split('-')[1]);
                        goal_differ = Math.abs(home_goal - away_goal);      // 进球差
                        match_home_name = cur_tr.find('td').eq(2).find('a').text();
                        home_position = (match_home_name === home_name) ? 0 : 1;
                        match_result = (home_goal >= away_goal) ? ((home_goal > away_goal) ? 3 : 1) : 0;
                        home_result = home_match_result(home_position, match_result);       // 主队该场比赛赛果
                        if (match_result === 3){
                            home_odd = cur_tr.find('td').eq(6).find('span').text();
                        } else {
                            home_odd = cur_tr.find('td').eq(6).text();
                        }
                        if (home_odd === '-' || home_odd === ''){
                            return true;
                        }
                         if (match_result === 1){
                            draw_odd = cur_tr.find('td').eq(7).find('span').text();
                        } else {
                            draw_odd = cur_tr.find('td').eq(7).text();
                        }
                        if (match_result === 0){
                            away_odd = cur_tr.find('td').eq(8).find('span').text();
                        } else {
                            away_odd = cur_tr.find('td').eq(8).text();
                        }
                        match_returnrate = compute_returnrate(home_odd, draw_odd, away_odd);
                        // console.log(match_returnrate)
                        home_pro = match_returnrate/home_odd;
                        draw_pro = match_returnrate/draw_odd;
                        away_pro = match_returnrate/away_odd;
                        home_vigour += multi_num * compute_vigour_change(home_position, home_result, home_pro, draw_pro, away_pro, goal_differ);
                        is_latest_match = false
                    });
                    is_latest_match = true;
                    $('.awaycomp tr:not(:hidden)').each(function(){
                        cur_tr = $(this);
                        if (cur_tr.attr('class') === "titlebg" || cur_tr.attr('class') === "tableh"){
                            return true;
                        }
                        match_timestamp = new Date(cur_tr.find('td').eq(1).find('a').text().replace(/-/g,'/')).getTime()/ 1000;
                        if ((current_timestamp - match_timestamp) > limit_day*86400){
                            return true;
                        }
                        differ_day = (current_timestamp - match_timestamp)/86400;       // 距今几天
                        multi_num = Math.pow(1.1, -differ_day);        // 分数乘积
                        score = cur_tr.find('td').eq(3).text();
                        home_goal = parseInt(score.split('-')[0]);
                        away_goal = parseInt(score.split('-')[1]);
                        goal_differ = Math.abs(home_goal - away_goal);      // 进球差
                        match_home_name = cur_tr.find('td').eq(2).find('a').text();
                        away_position = (match_home_name === away_name) ? 0 : 1;
                        match_result = (home_goal >= away_goal) ? ((home_goal > away_goal) ? 3 : 1) : 0;
                        away_result = home_match_result(away_position, match_result);       // 客队该场比赛赛果
                        if (match_result === 3){
                            home_odd = cur_tr.find('td').eq(6).find('span').text();
                        } else {
                            home_odd = cur_tr.find('td').eq(6).text();
                        }
                         if (home_odd === '-' || home_odd === ''){
                            return true;
                        }
                         if (match_result === 1){
                            draw_odd = cur_tr.find('td').eq(7).find('span').text();
                        } else {
                            draw_odd = cur_tr.find('td').eq(7).text();
                        }
                        if (match_result === 0){
                            away_odd = cur_tr.find('td').eq(8).find('span').text();
                        } else {
                            away_odd = cur_tr.find('td').eq(8).text();
                        }
                        match_returnrate = compute_returnrate(home_odd, draw_odd, away_odd)
                        // console.log(match_returnrate)
                        home_pro = match_returnrate/home_odd;
                        draw_pro = match_returnrate/draw_odd;
                        away_pro = match_returnrate/away_odd;
                        away_vigour += multi_num * compute_vigour_change(away_position, away_result, home_pro, draw_pro, away_pro, goal_differ);
                        is_latest_match = false
                    });
                    // console.log(home_vigour.toFixed(3));
                    // console.log(away_vigour.toFixed(3));
                    // console.log(home_vigour - away_vigour);
                    vigour_dict = {
                        'vigour_difference' : parseFloat((home_vigour - away_vigour).toFixed(3))
                    };
                    return vigour_dict
    
                    """
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
                        this_match_handicap_num=this_match_handicap_num,
                        handicap_home_odd=handicap_home_odd,
                        handicap_away_odd=handicap_away_odd,
                        vigour_difference=current_handicap_dict['vigour_difference'],
                    )
                    if coll.find({'match_id': match_id}).count() == 0:
                        coll.insert(insertItem)
                driver.close()
                windows = driver.window_handles
                driver.switch_to.window(windows[0])

    # 关闭窗口
    driver.quit()

except Exception as err:
    print('%s\n%s' % (err, traceback.format_exc()))
finally:
    mongo_client.close()



