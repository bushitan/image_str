# -*- coding: utf-8 -*-
import httplib, urllib,urllib2
import json
if __name__ == '__main__':

    #http://127.0.0.1:8000/art/wx_img_str
    httpClient = None
    try:

        # url = "http://127.0.0.1:8000/art/wx_img_str"
        # url = "http://127.0.0.1:8000/weixin/"
        # url = 'http://120.27.97.33/weixin/'
        url = 'http://127.0.0.1:8000/grid/api/img_str/'
        data  = {  "img_url":"http://mmbiz.qpic.cn/mmbiz/EmT9585IibD0V5dic327aVTjBFr1PgAcdzb7SDPK0Ndo3qqm26wHn6s4Qpf5TddjtpNFRrmL8CBb8Q64XuN13v4Q/0"}
        req = urllib2.Request(url)
        data = urllib.urlencode(data)
        #enable cookie
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        response = opener.open(req, data)
        res = response.read()
        print response.read()
        obj = json.loads(res)
        print obj['img_url']
        print obj['str_url']
    except Exception, e:
        print e
    finally:
        if httpClient:
            httpClient.close()