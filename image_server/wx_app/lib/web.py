# -*- coding: utf-8 -*-
import  image_server.settings as SETTINGS
import httplib, urllib,urllib2

def DownFile(img_resize_url,img_path):
    # img_down_path =
    # img_down_path = CreateFileName(re_name)["local_path"]
    f = urllib2.urlopen(img_resize_url)
    data = f.read()
    with open(img_path, "wb") as code:
        code.write(data)
    # return img_down_path