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
import redis


# 参数
company_name_dict = {
    # 'Crown': 'Crown',
    'Bet365': 'bet365',
     '易胜博': 'yishengbo',
    '韦德': 'weide',
    '明陞': 'mingsheng',
    '10BET': 'bet10',
    '金宝博': 'jinbaobo',
    '12bet': 'bet12',
    '利记': 'liji',
    '盈禾': 'yinghe',
    # '18Bet': 'bet18',
    '立博': 'ladbrokes',
}

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
                yield SplashRequest(url, self.parse, args={'wait': 0.5, 'images': 0, 'timeout': 30, 'lua_source': LUA_SCRIPT}, dont_filter=True)
            except Exception as err:
                print('%s\n%s' % (err, traceback.format_exc()))
    #
    # '''
    #     redis中存储的为set类型的公司名称，使用SplashRequest去请求网页。
    #     注意：不能在make_request_from_data方法中直接使用SplashRequest（其他第三方的也不支持）,会导致方法无法执行，也不抛出异常
    #     但是同时重写make_request_from_data和make_requests_from_url方法则可以执行
    # '''

    def parse(self, response):
        try:
            match_id = response.url.split('=')[-1]
            trs = response.xpath('//table[@id="odds"]/tbody/tr')
            # 存入模型
            single_match_item = QiutanOriginOddsItem()
            single_match_item['match_id'] = match_id
            for tr in trs:
                if len(tr.xpath('td')) != 12 or len( tr.xpath('td')[0].xpath('text()')) == 0:
                    continue
                current_company_name = tr.xpath('td')[0].xpath('text()').extract()[0].strip()
                if current_company_name in company_name_dict.keys():
                    company_nickname = company_name_dict[current_company_name]
                    # 赔率部分
                    origin_over_key = company_nickname + '_origin_over'
                    origin_goal_handicap_key = company_nickname+'_origin_goal_handicap'
                    origin_under_key = company_nickname+'_origin_under'
                    last_over_key = company_nickname+'_last_over'
                    last_goal_handicap_key = company_nickname+'_last_goal_handicap'
                    last_under_key = company_nickname+'_last_under'
                    single_match_item[origin_over_key] = float(tr.xpath('td')[2].xpath('text()').extract()[0])
                    single_match_item[origin_goal_handicap_key] = MyTools.convert_goal_handicap(tr.xpath('td')[3].xpath('text()').extract()[0])
                    single_match_item[origin_under_key] = float(tr.xpath('td')[4].xpath('text()').extract()[0])
                    single_match_item[last_over_key] = float(tr.xpath('td')[8].xpath('text()').extract()[0])
                    single_match_item[last_goal_handicap_key] = MyTools.convert_goal_handicap(tr.xpath('td')[9].xpath('text()').extract()[0])
                    single_match_item[last_under_key] = float(tr.xpath('td')[10].xpath('text()').extract()[0])
            if 'bet365_origin_over' in single_match_item.keys():
                yield single_match_item
            else:
                r = redis.Redis(host='localhost', port=6381, db=0)
                return_url = response.url.split('url=')[1]
                r.lpush('qiutan_analysis:start_urls', return_url)
                print('没获取到bet365, 重新推入队列！！！%s' % return_url)
        except Exception as err:
            print('%s\n%s' % (err, traceback.format_exc()))
            r = redis.Redis(host='localhost', port=6381, db=0)
            return_url = response.url.split('url=')[1]
            r.lpush('qiutan_analysis:start_urls', return_url)
            print('重新推入队列！！！%s' % return_url)
            return False
            # pdb.set_trace()



