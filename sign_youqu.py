#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import os
import random
import requests
import six
import sys
import time


LOG_FILE = os.path.join(os.path.split(os.path.abspath(__file__))[0],
                        "sign_youqu.log")
LOG = logging.getLogger(__name__)


users  = []
users.append({"name": "张洪涛", "id": "9593"})
group_ids = ["2001116"]


class Client(object):
    """HTTP client.
    """
    def _json_request(self, method, path, **kwargs):
        url = ''.join([path])
        url_info = "Request url ...%s" % url
        LOG.debug(url_info)

        response = requests.request(method, url, **kwargs)
        response_info = "Got response:%s" % response
        LOG.debug(response_info)

        body = response.content
        try:
            body = json.loads(body)
        except ValueError:
            LOG.debug('Could not decode response body as JSON')

        return response, body

    def get(self, url, **kwargs):
        return self._json_request("GET", url, **kwargs)

    def post(self, url, **kwargs):
        return self._json_request("POST", url, **kwargs)

    def put(self, url, **kwargs):
        return self._json_request("PUT", url, **kwargs)

    def delete(self, url, **kwargs):
        return self._json_request('DELETE', url, **kwargs)


class genarate_pos():
    def __init__(self):
        """
        左上角坐标: 114.391847,30.518829
        """
        self.start_x = 114.391847
        self.start_y = 30.518829
        self.max_offset_x = 0.011426
        self.max_offset_y = 0.006284

    def get_random_pos(self):
        return (self.start_x + random.uniform(0, self.max_offset_x),
                self.start_y + random.uniform(0, self.max_offset_y))


def translate_pos(c, x, y):
    baidu_url = "http://api.map.baidu.com/geocoder/v2/?ak=Es0Zdh4LrqUwnh" \
             "8ylnxCXd44oNFZhcxA&location=" \
             "%s,%s&output=json&pois=1" % (y, x)
    resp, body = c.get(baidu_url)
    return body["result"]["pois"][0]["name"]


def setup_log():
    FORMAT = '%(asctime)s | %(levelname)s | %(lineno)04d | %(message)s'
    logging.basicConfig(
        level=logging.INFO,
        filename=LOG_FILE,
        filemode='a',
        format=FORMAT)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter(FORMAT)
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


def sign(c, user_name, user_id, group_id, pos_name, x, y):
    url = "http://iyouqu.com.cn:8080/app/group/service.do"
    pos_str = "在%s签到啦！" % pos_name.encode('utf-8')
    params = {
            "groupId": group_id,
            "imei": "YADAqI8BoxFuYzwdens2tA==",
            "userName": user_name,
            "userId": user_id,
            "msgId": "APP086",
            "position": pos_str,
            "longitude": round(x, 6),
            "latitude": round(y, 6)
            }
    data = json.dumps(params, sort_keys=False, separators=(',', ':'),
                      ensure_ascii=False)
    body = {"text": data}
    return c.post(url, data=body)


def share_target(c):
    # url = "http://iyouqu.com.cn:8080/app/group/service.do"
    url = "http://common.iyouqu.com.cn:8080/app/group/service.do"
    params = {
            "content": "http://www.baidu.com",
            "userId": user_id, # "9593"
            "groupName": "文件小助手", # 发言混经验群 2001116
            "msgId": "APP083",
            "isOriginal": True,
            "groupId": 1006520,
            "type": 11,
            "isForward": True
            }
    data = json.dumps(params, sort_keys=False, separators=(',', ':'),
                      ensure_ascii=False)
    print data
    body = {"text": data}
    return c.post(url, data=body)

def user_login(c):
    """
    用户登录
    :param c:
    :return:
    """
    url = "http://iyouqu.com.cn:8080/app/user/service.do"
    params = {"device":"Che1-CL20","mobile":"13720303173","msgId":"APP129","password":"3c770b02ca2dc720193bf4fc699423f3","registrationId":"86c7d84348678164f6c2696d86bd5862","system":"4.4.4","systemType":"1","version":"V2.0.10"}
    data = json.dumps(params, sort_keys=False, separators=(',', ':'),
                      ensure_ascii=False)
    # print data
    body = {"text": data}
    return c.post(url, data=body)


def set_up():
    setup_log()
    return Client()


def do_work(c):
    resp, body = user_login(c)
    zh_body = json.dumps(body).decode("unicode_escape")
    LOG.info("login in youqu, resp: %s, body: %s", resp, zh_body)

    for user in random.sample(users, len(users)):
        for group_id in group_ids:
            x, y = genarate_pos().get_random_pos()
            pos_name = translate_pos(c, x, y)
            sign_resp, sign_body = sign(c, user['name'], user['id'],
                                        group_id, pos_name, x, y)
            zh_body = json.dumps(sign_body).decode("unicode_escape")
            LOG.info("User %(name)s :sign in youqu, resp: %(resp)s, "
                     "body: %(body)s", {'name': user['name'],
                                        'resp': sign_resp,
                                        'body': sign_body})
        time.sleep(random.randint(0, 5) * 60)


def main():
    c = set_up()
    do_work(c)

if __name__ == "__main__":
    sys.exit(main())

