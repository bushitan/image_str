# -*- coding: utf-8 -*-
import httplib, urllib,urllib2
from lib.magick import Magick

import os
from wx_app.lib.filepath import FilePath
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE_PATH = FilePath(BASE_DIR)

import json
from PIL import Image

if __name__ == '__main__':

    #http://127.0.0.1:8000/art/wx_img_str
    httpClient = None
    try:
        #下载文件
        url = "http://7xsark.com1.z0.glb.clouddn.com/12_20161124144609.mp4"
        name = str(url).split("/")[-1]
        img_down_path = FILE_PATH.Down(name)["local_path"]
        f = urllib2.urlopen(url)
        data = f.read()
        with open(img_down_path, "wb") as code:
            code.write(data)

        #视频转换
        img_type = "gif"
        user_id = 59
        img_up_path = FILE_PATH.Up(img_type,user_id) #按用户id命名图片
        # print
        magick = Magick(img_up_path["local_path"])
        magick.Video2Gif(0,6,img_down_path)


        url = 'https://www.12xiong.top/wx_app/img/query/'

        data  = {  "img_url":"http://7xsark.com1.z0.glb.clouddn.com/0_20161025165325.gif"}
        data  = {  "img_url":"http://7xsark.com1.z0.glb.clouddn.com/yuan.gif?imageMogr2/thumbnail/170x240"}

        data = {
            'uid': 10 ,
            'category_id': 'null',
        }


        # req = urllib2.Request(url)
        # data = urllib.urlencode(data)
        # #enable cookie
        # opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        # response = opener.open(req,data)
        # res = response.read()
        # print res
        # obj = json.loads(res)
        # print obj['img_url']
        # print obj['str_url']
    except Exception, e:
        print e
    finally:
        if httpClient:
            httpClient.close()