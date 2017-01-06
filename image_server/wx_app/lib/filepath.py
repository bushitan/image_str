# -*- coding: utf-8 -*-
import time
import  image_server.settings as SETTINGS
class FilePath():
    BASE_DIR  = ''
    def __init__(self,BASE_DIR):
        self.BASE_DIR = BASE_DIR
    def Up(self,type ,uid = 0 ):
        _type = type
        # _img_filedir = self.BASE_DDIR + "/wx_app/static/magick/upload/"
        _img_filedir = SETTINGS.MAGICK_FILE
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
        # _img_filedir = self.BASE_DIR + "/wx_app/static/magick/upload/"
        _img_filedir = SETTINGS.MAGICK_FILE
        _img_localpath = _img_filedir + name
        return {
            "local_path":_img_localpath,
        }

    def GetMagickPy(self):
        return self.BASE_DIR + "/wx_app/lib/magick.py"


def CreateFileName(type ,uid = 0 ):
    _type = type
    _img_filedir = SETTINGS.MAGICK_FILE
    _img_name = str(uid) + "_" + "{}".format(time.strftime('%Y%m%d%H%M%S'))
    _img_style = "." + _type
    _img_filename = _img_name+_img_style
    _img_localpath = _img_filedir + _img_filename
    return {
        "name":_img_name,  # 文件命名  12_1250125
        "file_name":_img_filename,# 文件全名  12_1250125.jpg
        "type":_type, #  文件类型 .jpg
        "local_path":_img_localpath,  # 本地路径  c:\image_server/static/12_1250125.jpg
    }
