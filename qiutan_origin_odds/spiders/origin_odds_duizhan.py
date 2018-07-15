# -*- coding: utf-8 -*-
import scrapy
import pdb
from qiutan_origin_odds.items import QiutanOriginOddsItem
from scrapy_splash import SplashRequest
from qiutan_origin_odds.spiders.tools import MyTools
from scrapy_redis.spiders import RedisSpider
from pymongo import MongoClient
import traceback
import time

# 参数
Sa = 10
Sb = 3

# scrapy crawl origin_odds
# class OriginOddsSpider(scrapy.Spider):
class OriginOddsSpider(RedisSpider):
    # name = 'origin_odds'
    allowed_domains = ['http://zq.win007.com']
    start_urls = []
    redis_key = 'qiutan_analysis:start_urls'
    global splashurl
    splashurl = "http://192.168.99.100:8050/render.html"


    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield scrapy.Request(url)
    # # 此处是重父类方法，并使把url传给splash解析
    def make_requests_from_url(self, url):
        global splashurl
        url = splashurl + "?url=" + url
        # 使用代理访问
        proxy = MyTools.get_proxy()
        LUA_SCRIPT = """
                            function main(splash)
                                splash:on_request(function(request)
                                    request:set_proxy{
                                        host = "%(host)s",
                                        port = %(port)s,
                                        username = '', password = '', type = "HTTPS",
                                    }
                                    request:set_header('X-Forwarded-For', %(proxy_ip)s)
                                end)
                                assert(splash:go(args.url))
                                assert(splash:wait(1))
                                return {
                                    html = splash:html(),
                                }
                            end
                            """
        try:
            proxy_host = proxy.strip().split(':')[0]
            proxy_port = int(proxy.strip().split(':')[-1])
            LUA_SCRIPT = LUA_SCRIPT % {'host': proxy_host, 'port': proxy_port, 'proxy_ip': proxy_host}
            print('make_requests代理为：', "http://{}".format(proxy))
            return SplashRequest(url, self.parse,
                                 args={'wait': 0.5, 'images': 0, 'timeout': 30, 'lua_source': LUA_SCRIPT},
                                 dont_filter=True)
        except Exception as err:
            MyTools.delete_proxy(proxy)
            print('%s\n%s' % (err, traceback.format_exc()))

    def start_requests(self):
        for url in self.start_urls:
            # 使用代理访问
            proxy = MyTools.get_proxy()

            LUA_SCRIPT = """
                        function main(splash)
                            splash:on_request(function(request)
                                request:set_proxy{
                                    host = "%(host)s",
                                    port = %(port)s,
                                    username = '', password = '', type = "HTTPS",
                                }
                                request:set_header('X-Forwarded-For', %(proxy_ip)s)
                            end)
                            assert(splash:go(args.url))
                            assert(splash:wait(1))
                            return {
                                html = splash:html(),
                            }
                        end
                        """
            proxy_host = proxy.strip().split(':')[0]
            proxy_port = int(proxy.strip().split(':')[-1])
            LUA_SCRIPT = LUA_SCRIPT % {'host': proxy_host, 'port': proxy_port, 'proxy_ip': proxy_host}
            try:
                print('初始代理为：', "http://{}".format(proxy))
                yield SplashRequest(url, self.parse, args={'wait': 0.5, 'images': 0, 'timeout': 30, 'lua_source': LUA_SCRIPT}, dont_filter=True)
            except Exception as err:
                MyTools.delete_proxy(proxy)
                print('%s\n%s' % (err, traceback.format_exc()))
    #
    # '''
    #     redis中存储的为set类型的公司名称，使用SplashRequest去请求网页。
    #     注意：不能在make_request_from_data方法中直接使用SplashRequest（其他第三方的也不支持）,会导致方法无法执行，也不抛出异常
    #     但是同时重写make_request_from_data和make_requests_from_url方法则可以执行
    # '''

    def parse(self, response):
        try:
            match_id = response.url.split('/')[-1].split('.')[0]
            league_name = response.xpath('//span[@class="LName"]/text()').extract()[0]
            home_name = response.xpath('//div[@class="home"]').xpath('a/text()').extract()[0].split('(')[0]
            home_team_id = response.xpath('//div[@class="home"]').xpath('a/@href').extract()[0].split('/')[-1].split('.')[0]
            away_name = response.xpath('//div[@class="guest"]').xpath('a/text()').extract()[0]
            away_team_id = response.xpath('//div[@class="guest"]').xpath('a/@href').extract()[0].split('/')[-1].split('.')[0]
            home_origin_odd = float(response.xpath('//tr[@id="tr_o_1_8"]/td')[2].xpath('text()').extract()[0])
            draw_origin_odd = float(response.xpath('//tr[@id="tr_o_1_8"]/td')[3].xpath('text()').extract()[0])
            away_origin_odd = float(response.xpath('//tr[@id="tr_o_1_8"]/td')[4].xpath('text()').extract()[0])
        except Exception as err:
            print('%s\n%s' % (err, traceback.format_exc()))
            return False
            # pdb.set_trace()
        if len(response.xpath('//div[@id="headVs"]/text()')) == 0:
            is_finished = True
        else:
            is_finished = False
        if is_finished:
            home_goal = int(response.xpath('//div[@id="headVs"]/div[@class="end"]/div[@class="score"]')[0].xpath('text()').extract()[0])
            away_goal = int(response.xpath('//div[@id="headVs"]/div[@class="end"]/div[@class="score"]')[1].xpath('text()').extract()[0])
            if home_goal > away_goal:
                result = 3
            elif home_goal < away_goal:
                result = 0
            else:
                result = 1
        else:
            result = '未结束'
        start_time = response.xpath('//div[@class="vs"]/div')[0].xpath('text()')[1].extract().split(' ')[1].split('\xa0')[0] + ' ' + response.xpath('//div[@class="vs"]/div')[0].xpath('text()')[1].extract().split(' ')[1].split('\xa0')[1]
        start_time_array = time.strptime(start_time, "%Y-%m-%d %H:%M")
        start_time_stamp = time.mktime(start_time_array)
        # 历史交锋
        live_tr_list = response.xpath('//table[@id="table_v"]/tbody/tr')
        for live_tr in live_tr_list:
            try:
                if len(live_tr.xpath('td')) != 15:
                    continue
                live_tr_id = live_tr.xpath('td')[3].xpath('a/@href').extract()[0].split('/')[-1].split('.')[0]
                # if live_tr_id == match_id:
                #     continue
                current_start_time = '20' + live_tr.xpath('td')[1].xpath('text()').extract()[0]
                current_start_time_array = time.strptime(current_start_time, "%Y-%m-%d")
                current_start_time_stamp = time.mktime(current_start_time_array)
                # 超过1年就跳过
                if (start_time_stamp - current_start_time_stamp) > 31622400:
                    break

                url = 'http://bf.win007.com/detail/%s.htm' % live_tr_id
                # 开始跳转页面
                single_match_base_info_dict = dict(match_id=match_id, league_name=league_name, home_name=home_name, home_team_id=home_team_id, away_name=away_name, away_team_id=away_team_id, start_time=start_time,
                                                   data_type=0, result=result, home_origin_odd=home_origin_odd, draw_origin_odd=draw_origin_odd, away_origin_odd=away_origin_odd)
                proxy = MyTools.get_proxy()
                LUA_SCRIPT = """
                                                                                function main(splash)
                                                                                    splash:on_request(function(request)
                                                                                        request:set_proxy{
                                                                                            host = "%(host)s",
                                                                                            port = %(port)s,
                                                                                            username = '', password = '', type = "HTTPS",
                                                                                        }
                                                                                        request:set_header('X-Forwarded-For', %(proxy_ip)s)
                                                                                    end)
                                                                                    assert(splash:go(args.url))
                                                                                    assert(splash:wait(1))
                                                                                    return {
                                                                                        html = splash:html(),
                                                                                    }
                                                                                end
                                                                                """
                proxy_host = proxy.strip().split(':')[0]
                proxy_port = int(proxy.strip().split(':')[-1])
                LUA_SCRIPT = LUA_SCRIPT % {'host': proxy_host, 'port': proxy_port, 'proxy_ip': proxy_host}
                print('单场比赛实力信息代理为：', "http://{}".format(proxy))
                yield SplashRequest(url, self.detail_parse, meta=single_match_base_info_dict,
                                    args={'wait': 0.5, 'images': 0, 'timeout': 30, 'lua_source': LUA_SCRIPT},
                                    dont_filter=True)

            except Exception as err:
                print('%s\n%s' % (err, traceback.format_exc()))

        # 主队
        history1_tr_list = response.xpath('//table[@id="table_hn"]/tbody/tr')
        # inc_1 = 0
        for history1_tr in history1_tr_list:
            try:
                # if inc_1 > 2:
                #     break
                if len(history1_tr.xpath('td')) != 15:
                    continue
                history1_tr_id = history1_tr.xpath('td')[3].xpath('a/@href').extract()[0].split('/')[-1].split('.')[0]
                # if history1_tr_id == match_id:
                #     continue

                current_start_time = '20' + history1_tr.xpath('td')[1].xpath('text()').extract()[0]
                current_start_time_array = time.strptime(current_start_time, "%Y-%m-%d")
                current_start_time_stamp = time.mktime(current_start_time_array)
                # 超过2个星期就跳过
                if (start_time_stamp - current_start_time_stamp) > 1209600:
                    break

                url = 'http://bf.win007.com/detail/%s.htm' % history1_tr_id
                # 开始跳转页面
                single_match_base_info_dict = dict(match_id=match_id, league_name=league_name, home_name=home_name, home_team_id=home_team_id, away_name=away_name, away_team_id=away_team_id, start_time=start_time,
                                                   data_type=1, result=result, home_origin_odd=home_origin_odd, draw_origin_odd=draw_origin_odd, away_origin_odd=away_origin_odd)
                proxy = MyTools.get_proxy()
                LUA_SCRIPT = """
                                                                                        function main(splash)
                                                                                            splash:on_request(function(request)
                                                                                                request:set_proxy{
                                                                                                    host = "%(host)s",
                                                                                                    port = %(port)s,
                                                                                                    username = '', password = '', type = "HTTPS",
                                                                                                }
                                                                                                request:set_header('X-Forwarded-For', %(proxy_ip)s)
                                                                                            end)
                                                                                            assert(splash:go(args.url))
                                                                                            assert(splash:wait(1))
                                                                                            return {
                                                                                                html = splash:html(),
                                                                                            }
                                                                                        end
                                                                                        """
                proxy_host = proxy.strip().split(':')[0]
                proxy_port = int(proxy.strip().split(':')[-1])
                LUA_SCRIPT = LUA_SCRIPT % {'host': proxy_host, 'port': proxy_port, 'proxy_ip': proxy_host}
                print('单场比赛实力信息代理为：', "http://{}".format(proxy))
                yield SplashRequest(url, self.detail_parse, meta=single_match_base_info_dict,
                                    args={'wait': 0.5, 'images': 0, 'timeout': 30, 'lua_source': LUA_SCRIPT},
                                    dont_filter=True)
                # inc_1 += 1

            except Exception as err:
                print('%s\n%s' % (err, traceback.format_exc()))
        # 客队
        history2_tr_list = response.xpath('//table[@id="table_an"]/tbody/tr')
        # inc_2 = 0
        for history2_tr in history2_tr_list:
            try:
                # if inc_2 > 2:
                #     break
                if len(history2_tr.xpath('td')) != 15:
                    continue
                history2_tr_id = history2_tr.xpath('td')[3].xpath('a/@href').extract()[0].split('/')[-1].split('.')[0]
                if history2_tr_id == match_id:
                    continue
                current_start_time = '20' + history2_tr.xpath('td')[1].xpath('text()').extract()[0]
                current_start_time_array = time.strptime(current_start_time, "%Y-%m-%d")
                current_start_time_stamp = time.mktime(current_start_time_array)
                # 超过2个星期就跳过
                if (start_time_stamp - current_start_time_stamp) > 1209600:
                    break

                url = 'http://bf.win007.com/detail/%s.htm' % history2_tr_id
                # 开始跳转页面
                single_match_base_info_dict = dict(match_id=match_id, league_name=league_name, home_name=home_name, home_team_id=home_team_id, away_name=away_name, away_team_id=away_team_id, start_time=start_time,
                                                   data_type=2, result=result, home_origin_odd=home_origin_odd, draw_origin_odd=draw_origin_odd, away_origin_odd=away_origin_odd)
                proxy = MyTools.get_proxy()
                LUA_SCRIPT = """
                                                                                                function main(splash)
                                                                                                    splash:on_request(function(request)
                                                                                                        request:set_proxy{
                                                                                                            host = "%(host)s",
                                                                                                            port = %(port)s,
                                                                                                            username = '', password = '', type = "HTTPS",
                                                                                                        }
                                                                                                        request:set_header('X-Forwarded-For', %(proxy_ip)s)
                                                                                                    end)
                                                                                                    assert(splash:go(args.url))
                                                                                                    assert(splash:wait(1))
                                                                                                    return {
                                                                                                        html = splash:html(),
                                                                                                    }
                                                                                                end
                                                                                                """
                proxy_host = proxy.strip().split(':')[0]
                proxy_port = int(proxy.strip().split(':')[-1])
                LUA_SCRIPT = LUA_SCRIPT % {'host': proxy_host, 'port': proxy_port, 'proxy_ip': proxy_host}
                print('单场比赛实力信息代理为：', "http://{}".format(proxy))
                yield SplashRequest(url, self.detail_parse, meta=single_match_base_info_dict,
                                    args={'wait': 0.5, 'images': 0, 'timeout': 30, 'lua_source': LUA_SCRIPT},
                                    dont_filter=True)
                # inc_2 += 1

            except Exception as err:
                print('%s\n%s' % (err, traceback.format_exc()))

    def detail_parse(self, response):
        league_name = response.meta['league_name']
        match_id = response.meta['match_id']
        home_name = response.meta['home_name']
        home_team_id = response.meta['home_team_id']
        away_name = response.meta['away_name']
        away_team_id = response.meta['away_team_id']
        start_time = response.meta['start_time']
        home_origin_odd = response.meta['home_origin_odd']
        draw_origin_odd = response.meta['draw_origin_odd']
        away_origin_odd = response.meta['away_origin_odd']
        data_type = response.meta['data_type']
        result = response.meta['result']
        try:
            current_home_team_id = response.xpath('//div[@id="home"]/a/@href').extract()[0].split('/')[-1].split('.')[0]
            current_away_team_id = response.xpath('//div[@id="guest"]/a/@href').extract()[0].split('/')[-1].split('.')[0]
        except Exception as err:
            print('%s\n%s' % (err, traceback.format_exc()))
            pdb.set_trace()
        # 比赛数据
        matchs_data_tr = response.xpath('//div[@id="matchData"]/div[@class="content"]')[3].xpath('table/tbody/tr')
        home_shemen = 0
        home_shezheng = 0
        home_attack = 0
        home_danger = 0
        away_shemen = 0
        away_shezheng = 0
        away_attack = 0
        away_danger = 0
        for item in matchs_data_tr:
            find_tds = item.xpath('td')
            if len(find_tds) != 5:
                continue
            get_data_name = find_tds[2].xpath('text()').extract()[0]
            if get_data_name == '射門':
                home_shemen = int(find_tds[1].xpath('text()').extract()[0])
                away_shemen = int(find_tds[3].xpath('text()').extract()[0])
            elif get_data_name == '射正':
                home_shezheng = int(find_tds[1].xpath('text()').extract()[0])
                away_shezheng = int(find_tds[3].xpath('text()').extract()[0])
            elif get_data_name == '進攻':
                home_attack = int(find_tds[1].xpath('text()').extract()[0])
                away_attack = int(find_tds[3].xpath('text()').extract()[0])
            elif get_data_name == '危險進攻':
                home_danger = int( find_tds[1].xpath('text()').extract()[0])
                away_danger = int(find_tds[3].xpath('text()').extract()[0])

        # home_shepian = home_shemen - home_shezheng
        # away_shepian = away_shemen - away_shezheng

        # 如果进攻数据为0，则跳过
        if home_attack == 0 or away_attack == 0:
            return False
        # 计算应该变化的积分
        # home_effective_attack_rate = round((home_shezheng * Sa + home_shepian * Sb) / home_attack, 4)
        # away_effective_attack_rate = round((away_shezheng * Sa + away_shepian * Sb) / home_attack, 4)
        # home_dangerous_attack_rate = round(home_danger / home_attack, 4)
        # away_dangerous_attack_rate = round(away_danger / away_attack, 4)
        # home_attack_point = home_effective_attack_rate * 50
        # away_attack_point = away_effective_attack_rate * 50
        # home_guard_point = (0.5 - away_dangerous_attack_rate) * 50
        # away_guard_point = (0.5 - home_dangerous_attack_rate) * 50
        # home_add_point = round(home_attack_point + home_guard_point, 4)
        # away_add_point = round(away_attack_point + away_guard_point, 4)

        # 判断加分方向
        # if data_type == 0 or data_type == 1:
        #     # 交锋页面
        #     if data_type == 0:
        #         # 当前主队在主场
        #         if current_home_team_id == home_team_id:
        #             home_point_change = home_add_point
        #             away_point_change = away_add_point
        #         # 当前主队在客场
        #         else:
        #             home_point_change = away_add_point
        #             away_point_change = home_add_point
        #     # 主队历史页面
        #     else:
        #         if current_home_team_id == home_team_id:
        #             home_point_change = home_add_point
        #             away_point_change = 0
        #         # 当前主队在客场
        #         else:
        #             home_point_change = away_add_point
        #             away_point_change = 0
        # # 客队历史页面
        # else:
        #     # 当前客队在主场
        #     if current_home_team_id == away_name:
        #         home_point_change = 0
        #         away_point_change = home_add_point
        #     # 当前客队在客场
        #     else:
        #         home_point_change = 0
        #         away_point_change = away_add_point

        single_match_item = QiutanOriginOddsItem()
        single_match_item['match_id'] = match_id
        single_match_item['league_name'] = league_name
        single_match_item['home_name'] = home_name
        single_match_item['away_name'] = away_name
        single_match_item['start_time'] = start_time
        single_match_item['result'] = result
        single_match_item['home_origin_odd'] = home_origin_odd
        single_match_item['draw_origin_odd'] = draw_origin_odd
        single_match_item['away_origin_odd'] = away_origin_odd
        if current_home_team_id == home_team_id:
            current_team = 'home'
            single_match_item['current_team'] = current_team
            single_match_item['shemen'] = home_shemen
            single_match_item['shezheng'] = home_shezheng
            single_match_item['attack'] = home_attack
            single_match_item['danger'] = home_danger
        elif current_home_team_id == away_team_id:
            current_team = 'away'
            single_match_item['current_team'] = current_team
            single_match_item['shemen'] = home_shemen
            single_match_item['shezheng'] = home_shezheng
            single_match_item['attack'] = home_attack
            single_match_item['danger'] = home_danger
        elif current_away_team_id == home_team_id:
            current_team = 'home'
            single_match_item['current_team'] = current_team
            single_match_item['shemen'] = away_shemen
            single_match_item['shezheng'] = away_shezheng
            single_match_item['attack'] = away_attack
            single_match_item['danger'] = away_danger
        elif current_away_team_id == away_team_id:
            current_team = 'away'
            single_match_item['current_team'] = current_team
            single_match_item['shemen'] = away_shemen
            single_match_item['shezheng'] = away_shezheng
            single_match_item['attack'] = away_attack
            single_match_item['danger'] = away_danger
        yield single_match_item


