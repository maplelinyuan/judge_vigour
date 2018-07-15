import requests
import json
import random
import pdb

class MyTools():
    def __init__(self):
        pass

    def list_average(mylist):
        num = len(mylist)
        sum_score = sum(mylist)
        ave_num = round(sum_score / num, 2)
        return ave_num

    def over_threshold_num(mylist, ave_num, threshold_value, direction):
        # direction=1,表示升高方向;   direction=-1,表示降低方向
        if direction == -1:
            over_num = len([i for i in mylist if (i - ave_num) < -threshold_value])
        elif direction == 1:
            over_num = len([i for i in mylist if (i - ave_num) > threshold_value])
        return over_num

    def convert_handicap(handicap_name):
        handicap_name_dict = {
            '*三球': -3,
            '*两球半/三': -2.75,
            '*两球半': -2.5,
            '*两/两球半': -2.25,
            '*两球': -2,
            '*球半/两': -1.75,
            '*球半': -1.5,
            '*一/球半': -1.25,
            '*一球': -1,
            '*半/一': -0.75,
            '*半球': -0.5,
            '*平/半': -0.25,
            '平手': 0,
            '平/半': 0.25,
            '半球': 0.5,
            '半/一': 0.75,
            '一球': 1,
            '一/球半': 1.25,
            '球半': 1.5,
            '球半/两': 1.75,
            '两球': 2,
            '两/两球半': 2.25,
            '两球半': 2.5,
            '两球半/三': 2.75,
            '三球': 3,
        }
        return handicap_name_dict[handicap_name]

    def convert_goal_handicap(handicap_name):
        handicap_name_dict = {
            '0.5': 0.5,
            '0.5/1': 0.75,
            '1': 1,
            '1/1.5': 1.25,
            '1.5': 1.5,
            '1.5/2': 1.75,
            '2': 2,
            '2/2.5': 2.25,
            '2.5': 2.5,
            '2.5/3': 2.75,
            '3': 3,
            '3/3.5': 3.25,
            '3.5': 3.5,
            '3.5/4': 3.75,
            '4': 4,
            '4/4.5': 4.25,
            '4.5': 4.5,
            '4.5/5': 4.75,
            '5': 5,
        }
        return handicap_name_dict[handicap_name]

    def convert_result_text(result_text):
        if result_text == '勝':
            return 3
        elif result_text == '平':
            return 1
        elif result_text == '負':
            return 0
        else:
            return -1

    # api形式
    def get_proxy():
        proxy_total_num = 200
        proxy_index = random.randint(0, proxy_total_num - 1)
        proxy_list_text = requests.get(
            "http://127.0.0.1:8000/select?name=ipproxy.free_ipproxy&count={}".format(proxy_total_num)).content.decode()
        proxy_dict = json.loads(proxy_list_text)[proxy_index]
        proxy = proxy_dict['ip'] + ':' + str(proxy_dict['port'])
        return proxy
        # 第二个proxy_pool
        # return requests.get("http://127.0.0.1:5010/get/").content.decode()

    def delete_proxy(proxy):
        proxy_ip = proxy.split(':')[0]
        requests.get("http://127.0.0.1:8000/delete?name=ipproxy.free_ipproxy&ip={}".format(proxy_ip))
        # 第二个proxy_pool
        # requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy.decode()))

    # 文件形式
    # def get_proxy():
    #     proxy_index = random.randint(1, 256)
    #     with open('auto_odds_compare/proxy_list.txt', 'r', encoding='utf-8') as proxy_list_file:
    #         line_count = 1
    #         for line in proxy_list_file.readlines():
    #             if proxy_index == line_count:
    #                 get_proxy = line.strip()
    #                 break
    #             line_count += 1
    #     return get_proxy
    #
    # def delete_proxy(proxy):
    #     print('代理出错：', proxy)