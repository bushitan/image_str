# -*- coding: utf-8 -*-
import time
class FilePath():
    BASE_DIR  = ''
    def __init__(self,BASE_DIR):
        self.BASE_DIR = BASE_DIR
    def Up(self,type ,uid = 0 ):
        _type = type
        _img_filedir = self.BASE_DIR + "/wx_app/static/magick/upload/"
        _img_name = str(uid) + "_" + "{}".format(time.strftime('%Y%m%d%H%M%S'))
        _img_style = "." + _type
        _img_filename = _img_name+_img_style
        _img_localpath = _img_filedir + _img_filename
        return {
            "name":_img_name,
            "file_name":_img_filename,
            "type":_type,
            "local_path":_img_localpath,
        }

    def Down(self,name="1.gif"):
        _img_filedir = self.BASE_DIR + "/wx_app/static/magick/upload/"
        _img_localpath = _img_filedir + name
        return {
            "local_path":_img_localpath,
        }
