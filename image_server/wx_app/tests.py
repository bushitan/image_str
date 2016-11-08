# -*- coding: utf-8 -*-
import httplib, urllib,urllib2
import json
if __name__ == '__main__':

    #http://127.0.0.1:8000/art/wx_img_str
    httpClient = None
    try:

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