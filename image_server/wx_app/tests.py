# -*- coding: utf-8 -*-
import httplib, urllib,urllib2
import json
if __name__ == '__main__':

    #http://127.0.0.1:8000/art/wx_img_str
    httpClient = None
    try:

        app_id = "wx00098b11d40e8910"
        app_secret = "34362b7f79645d0659c5950e21e892cd"
        _code = "001yzWfg0Mlw9A1GH8jg0bhTfg0yzWfK"
        _session_url = "https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code "  %(app_id,app_secret,_code )
        print _session_url
        req = urllib2.Request(_session_url)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        response = opener.open(req)
        _json =  json.loads(response.read())
        print _json["errcode"]

        url = 'https://www.12xiong.top/wx_app/img/query/'

        data  = {  "img_url":"http://7xsark.com1.z0.glb.clouddn.com/0_20161025165325.gif"}
        data  = {  "img_url":"http://7xsark.com1.z0.glb.clouddn.com/yuan.gif?imageMogr2/thumbnail/170x240"}

        data = {
            'uid': 10 ,
            'category_id': 'null',
        }


        req = urllib2.Request(url)
        data = urllib.urlencode(data)
        #enable cookie
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        response = opener.open(req,data)
        res = response.read()
        print res
        # obj = json.loads(res)
        # print obj['img_url']
        # print obj['str_url']
    except Exception, e:
        print e
    finally:
        if httpClient:
            httpClient.close()