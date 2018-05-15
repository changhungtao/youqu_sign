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


def get_category_list(c):
    url = "http://iyouqu.com.cn:8080/app/newsActivity/service.do"
    params = {"msgId": "APP155",
              "menuId": 1}
    data = json.dumps(params, sort_keys=False, separators=(',', ':'),
                      ensure_ascii=False)
    # print data
    body = {"text": data}
    return c.post(url, data=body)


def get_category_obj_list(c):
    url = "http://iyouqu.com.cn:8080/app/newsActivity/service.do"
    params = {
            "userId": user_id,
            "msgId": "APP150",
            "department": "02A73000",
            "index": 60,
            "categoryType": 1,
            "categoryId": 21
            }
    data = json.dumps(params, sort_keys=False, separators=(',', ':'),
                      ensure_ascii=False)
    # print data
    body = {"text": data}
    return c.post(url, data=body)


def get_obj_detail(c, object_id):
    """object_id = 2346"""
    url = "http://iyouqu.com.cn:8080/app/newsActivity/service.do"
    params = {
             "msgId": "APP009",
             "objectId": object_id,
             "userId": user_id,
             "opinion": 0
             }
    data = json.dumps(params, sort_keys=False, separators=(',', ':'),
                      ensure_ascii=False)
    print data
    body = {"text": data}
    return c.post(url, data=body)


def get_target(c, pagesize, target_type, target_id):
    url = "http://iyouqu.com.cn:8080/app/service.do"
    params = {
            "index": "0",
            "msgId": "APP040",
            "pagesize": pagesize,
            "targetId": target_id,
            "targetType": target_type
            }
    data = json.dumps(params, sort_keys=False, separators=(',', ':'),
                      ensure_ascii=False)
    print data
    body = {"text": data}
    return c.post(url, data=body)


def discus_target(c, target_type, target_id):
    url = "http://iyouqu.com.cn:8080/app/service.do"
    params = {
            "content": "[微笑]顶！",
            "msgId": "APP039",
            "targetId": target_id,
            "targetType": target_type,
            "userId": user_id
            }
    data = json.dumps(params, sort_keys=False, separators=(',', ':'),
                      ensure_ascii=False)
    print data
    body = {"text": data}
    return c.post(url, data=body)


def chat_with_target(c):
    # url = "http://iyouqu.com.cn:8080/app/group/service.do"
    url = "http://common.iyouqu.com.cn:8080/app/group/service.do"
    params = {
            "content": "haha.",
            "userId": user_id,
            "groupName": "文件小助手",
            "msgId": "APP083",
            "isOriginal": True,
            "groupId": 1006520,
            "type": 1,
            "isForward": False
            }
    data = json.dumps(params, sort_keys=False, separators=(',', ':'),
                      ensure_ascii=False)
    print data
    body = {"text": data}
    return c.post(url, data=body)


def get_offline_msg(c):
    url = "http://common.iyouqu.com.cn:8080/app/group/service.do"
    params = {"msgId": "GET_OFFLINEMSG",
              "userId": "3514"}
    data = json.dumps(params, sort_keys=False, separators=(',', ':'),
                      ensure_ascii=False)
    print data
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


def vote(c):
    url = "http://iyouqu.com.cn:8080/app/service.do"
    params = {
             "activityId": "321",
             "answerList": [{
                "optionId": "2706",
                "topicId": "615"
             },
             {
                    "optionId": "2710",
                    "topicId": "616"
                },
                {
                    "optionId": "2715",
                    "topicId": "617"
                },
                {
                    "optionId": "2720",
                    "topicId": "618"
                },
                {
                    "optionId": "2723",
                    "topicId": "619"
                },
                {
                    "optionId": "2726",
                    "topicId": "620"
                },
                {
                    "optionId": "2729",
                    "topicId": "621"
                },
                {
                    "optionId": "2733",
                    "topicId": "622"
                },
                {
                    "optionId": "2737",
                    "topicId": "623"
                },
                {
                    "optionId": "2741",
                    "topicId": "624"
                }],
                "userId": "3514",
                "msgId": "APP018",
                "examDate": 19
            }

    data = json.dumps(params, sort_keys=False, separators=(',', ':'),
                      ensure_ascii=False)
    print data
    body = {"text": data}
    return c.post(url, data=body)


def get_menus(c):
    """
    获取菜单列表：
    type id name
    0 -1 最新
    0 -2 最热
    0 -3 活动
    1 1 公司
    1 26 观点
    1 36 人物
    1 3 党工团
    1 11 部门专题
    1 8 学堂
    0 -6 全部

    :param c:
    :return:
    """
    url = "http://iyouqu.com.cn:8080/app/newsActivity/service.do"
    params = {"msgId": "APP146"}
    data = json.dumps(params, sort_keys=False, separators=(',', ':'),
                      ensure_ascii=False)
    print data
    body = {"text": data}
    return c.post(url, data=body)


def get_activities(c):
    """
    获取活动列表
    :param c:
    :return:
    """
    url = "http://iyouqu.com.cn:8080/app/newsActivity/service.do"
    params = {
            "userId": "3514",
            "msgId": "APP150",
            "department": "02A73000",
            "index": 0,
            "categoryType": 0,
            "categoryId": -3
            }
    data = json.dumps(params, sort_keys=False, separators=(',', ':'),
                      ensure_ascii=False)
    print data
    body = {"text": data}
    return c.post(url, data=body)


def get_activitie_detail(c, active_id):
    """
    获取活动详情
    :param c:
    :param active_id: eg: 350
    :return:
    """
    url = "http://iyouqu.com.cn:8080/app/service.do"
    params = {"activityId": active_id, "index": "0", "msgId": "APP042"}
    data = json.dumps(params, sort_keys=False, separators=(',', ':'),
                      ensure_ascii=False)
    print data
    body = {"text": data}
    return c.post(url, data=body)


def join_activity(c):
    """
    参加活动投票
    :param c:
    :return:
    """
    url = "http://iyouqu.com.cn:8080/app/service.do"
    params = {
        "activityId": "346",
        "answerList": [{
            "optionId": "880", # 3058
            "topicId": "690",
            "topicType": 1
        }],
        "msgId": "APP018",
        "userId": "3514" # 9593 3514
    }
    # params = {"activityId":"321","answerList":[{"optionId":"2705","topicId":"615"},{"optionId":"2710","topicId":"616"},{"optionId":"2714","topicId":"617"},{"optionId":"2719","topicId":"618"},{"optionId":"2723","topicId":"619"},{"optionId":"2727","topicId":"620"},{"optionId":"2729","topicId":"621"},{"optionId":"2734","topicId":"622"},{"optionId":"2737","topicId":"623"},{"optionId":"2744","topicId":"624"}],"userId":"3514","msgId":"APP018","examDate":27}
    data = json.dumps(params, sort_keys=False, separators=(',', ':'),
                      ensure_ascii=False)
    print data
    body = {"text": data}
    return c.post(url, data=body)


def get_point_rule(c):
    """
    获取得分规则
    :param c:
    :return:
    """
    url = "http://iyouqu.com.cn:8080/app/service.do"
    params = {'msgId': 'POINT_RULE_INFO'}
    data = json.dumps(params, sort_keys=False, separators=(',', ':'),
                      ensure_ascii=False)
    body = {"text": data}
    return c.post(url, data=body)


def get_user_info(c, user_id):
    """
    获取用户信息
    :param c:
    :return:
    """
    url = "http://iyouqu.com.cn:8080/app/service.do"
    params = {'msgId': 'APP061', 'userId': user_id}
    data = json.dumps(params, sort_keys=False, separators=(',', ':'),
                      ensure_ascii=False)
    # print data
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
    # resp, body = share_target(c)
    # resp, body = get_target(c, 5, 1, "1993")
    # resp, body = get_category_obj_list(c)
    # resp, body = vote(c)
    # resp, body = get_offline_msg(c)

    """"个人经验值排名"""
    # all_score = []
    # for i in range(1, 1):
    # # for i in range(10000, 20000):
    #     # resp, body = user_login(c)
    #     resp, body = get_user_info(c, str(i)) #3655
    #     try:
    #         obj = body["resultMap"]["objList"][0]
    #         # LOG.info("%s %s", obj["id"], obj["name"])
    #         all_score.append(int(body["resultMap"]["total"]))
    #     except Exception:
    #         print body
    #     # zh_body = json.dumps(body, indent=4).decode("unicode_escape")
    #     zh_body = json.dumps(body).decode("unicode_escape")
    #     LOG.info("resp: %s, body: %s", resp, zh_body)
    # all_score.sort()
    # print all_score[-1]

    """查看活动详情"""
    # resp, body = get_activities(c)
    # obj_list = body["resultMap"]["objectList"]
    # for obj in obj_list:
    #     print obj["id"]
    #     resp, body = get_activitie_detail(c, obj["id"])
    #     zh_body = json.dumps(body, indent=4).decode("unicode_escape")
    #     LOG.info("resp: %s, body: %s", resp, zh_body)


    # resp, body = get_target(c, 2, "3578")
    # zh_body = json.dumps(body, indent=4).decode("unicode_escape")
    # LOG.info("resp: %s, body: %s", resp, zh_body)
    #
    # resp, body = discus_target(c, 2, "3578")
    # zh_body = json.dumps(body, indent=4).decode("unicode_escape")
    # LOG.info("resp: %s, body: %s", resp, zh_body)
    #
    # resp, body = get_target(c, 2, "3578")
    # zh_body = json.dumps(body, indent=4).decode("unicode_escape")
    # LOG.info("resp: %s, body: %s", resp, zh_body)

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
    """
    url = "http://localhost:57257"
    c = Client()
    resp, body = c.get("%s/v1/users" % url)
    baidu_url = ("http://api.map.baidu.com/geocoder/v2/?ak=Es0Zdh4LrqUwnh"
                 "8ylnxCXd44oNFZhcxA&callback=renderReverse&location="
                 "30.51585,114.39087&output=json&pois=1")
    """
    c = set_up()
#    from business_calendar import Calendar
#    import datetime
#
#    cal = Calendar()
#    while True:
#        now_obj = datetime.datetime.now()
#        if not cal.isworkday(now_obj.date()):
#            time.sleep(5)
#            continue
#        if now_obj.hour == 17 and now_obj.minute == 30:
#            LOG.info("Time to go home, and let's begin to sign in youqu.")
#            # Make a fake random time to sleep and do work
#            time.sleep(random.randint(0, 10) * 60)
#            do_work(c)
#        elif now_obj.hour == 8 and now_obj.minute == 0:
#            LOG.info("Time to do work, and let's begin to sign in youqu.")
#            # Make a fake random time to sleep and do work
#            time.sleep(random.randint(0, 10) * 60)
#            do_work(c)
#        # else:
#            # LOG.info("Not working time, no need to sign in youqu.")
#        time.sleep(5)

#    time.sleep(random.randint(0, 10) * 60)
    do_work(c)

if __name__ == "__main__":
    sys.exit(main())

