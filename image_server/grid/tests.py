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
        # url = 'http://127.0.0.1:8000/grid/api/img_str/'
        # url = 'http://120.27.97.33:91/grid/api/img_str/'
        _str_url = 'http://7xsark.com1.z0.glb.clouddn.com/str/20160706154945.png'
        img_url = 'http://avatar.csdn.net/2/8/B/1_u010085454.jpg'
        # url = "http://bushitan.pythonanywhere.com/art/show/?url=" + _str_url
        # url = "http://127.0.0.1:8001/art/show/?url=" + _str_url
        # url = "http://127.0.0.1:8000/grid/api/img_str_temp/?img_url=" + img_url
        # url = 'http://127.0.0.1:8000/grid/api/img_str_temp/'

        # url = 'http://127.0.0.1:8000/grid/api/img_str/'
        url = 'http://127.0.0.1:8000/grid/api/game/'

        # url = "http://127.0.0.1:8000/api/img_str/?img_url=" + img_url


        # data  = {  "img_url":"http://mmbiz.qpic.cn/mmbiz/EmT9585IibD0V5dic327aVTjBFr1PgAcdzb7SDPK0Ndo3qqm26wHn6s4Qpf5TddjtpNFRrmL8CBb8Q64XuN13v4Q/0"}
        data  = {  "img_url":"http://127.0.0.1:8000/static/art/img/20160706154153.png"}


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