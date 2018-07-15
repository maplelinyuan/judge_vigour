host = '235.32.123.55'
port = 6666

_script = """
           function main(splash)
             splash:on_request(function(request)
               request:set_proxy{{
                   host = "{host}",
                   port = {port},
                   username = '', password = '', type = "HTTPS",
               }}
               request:set_header('X-Forwarded-For', "{proxy_ip}")
             end)
             assert(splash:go(splash.args.url))
             assert(splash:wait(0.5))
             splash:runjs('document.querySelectorAll("td.lsm2")[{cur_index}].click()')
             splash:wait(3)
             return {{
                {my_html}
                }}
           end
           """.format(host=host, port=port, proxy_ip=host, cur_index=4, my_html='html=splash:html()')
print(_script)

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
LUA_SCRIPT = LUA_SCRIPT % {'host': host, 'port': port, 'proxy_ip': host}
# print(LUA_SCRIPT)