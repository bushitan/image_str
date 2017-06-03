#coding:utf-8
from django.views.generic import ListView
from wx_app.lib.qi_niu import QiNiu
import image_server.settings as SETTING
from django.http import HttpResponse
from wx_app.models import *
import json
import logging
import os
import time
from wx_app.lib.filepath import FilePath
logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE_PATH = FilePath(BASE_DIR)


import qiniu
from image_server.settings import (qiniu_access_key,qiniu_secret_key,qiniu_bucket_name)
#配置七牛的token，
def GetQiNiuToken(qiniu_path,filename):
    q = qiniu.Auth(qiniu_access_key, qiniu_secret_key)
    key = qiniu_path + filename
    policy = {
        "callbackUrl":"https://www.12xiong.top/qiniu/upload/",
        "callbackBody":"key=$(key)&hash=$(etag)&w=$(imageInfo.width)&h=$(imageInfo.height)&duration=$(avinfo.video.duration)&fsize=$(fsize)&vw=$(avinfo.video.width)&vh=$(avinfo.video.height)",
        "callbackHost":"120.27.97.33",
        "fsizeLimit": 6815744,
        # "mimeLimit": "image/png"
    }
    token = q.upload_token(qiniu_bucket_name,key = key,policy = policy)
    # token = q.upload_token(qiniu_bucket_name,key = key)
    return token,key

#配置上传图片名字
def UpFileName(img_type ,uid = 0 ):
        _type = img_type
        _img_name = str(uid) + "_" + "{}".format(time.strftime('%Y%m%d%H%M%S'))
        _img_style = "." + _type
        _img_filename = _img_name+_img_style
        return {
            "file_name":_img_filename,
        }

KEY_USER_HASH = {} #内存，key-session对应表


class QiNiuUpload( ListView):
    def get(self, request, *args, **kwargs):
        session = request.GET['session']
        _type = request.GET['type']
        _upload_info =  request.POST.get('upload_info',"")
        # _category_id = request.GET['category_id']

        # return HttpResponse(json.dumps({"status":"true"}),content_type="application/json")
        #小程序独有过滤
        if _type == "ext-mp4":
                _type = "mp4"

        # 1 查询用户是否存在
        if  User.objects.filter( session = session).exists() is False:
            return HttpResponse( json.dumps({"status":"false","msg":u"用户不存在"}),content_type="application/json" )
        _user = User.objects.get( session = session)
        print _type,_user.id
        #设置上传路径
        _up_path = UpFileName(_type,_user.id)
        token,key = GetQiNiuToken("",_up_path["file_name"])

        #保存图片用户数据
        KEY_USER_HASH[key] = {
            "uid":_user,
            "type":_type,
            "upload_info":_upload_info,
        }
        return HttpResponse(json.dumps({"status":"true","token":token,"key":key, "upload_info":_upload_info,}),content_type="application/json")
    def post(self, request, *args, **kwargs):
        try:
            key = request.POST['key']
            _hash = request.POST['hash']
            w = request.POST['w']
            h = request.POST['h']
            duration = request.POST['duration']
            fsize = request.POST['fsize']
            vw = request.POST['vw']
            vh = request.POST['vh']

            if duration == "" :
                duration = 0.0
            else :
                duration = float(duration)
            if w == "" :
                w = 0
            else :
                w = int(w)
            if h == "" :
                h = 0
            else :
                h = int(h)

            #图片存数据库
            if KEY_USER_HASH.has_key(key):
                _user = KEY_USER_HASH[key]["uid"]
                _type = KEY_USER_HASH[key]["type"]
                _category_id = KEY_USER_HASH[key]["category_id"]
                if KEY_USER_HASH[key]["upload_info"] == "":
                    _upload_info = {"type":0}
                else:
                    _upload_info = KEY_USER_HASH[key]["upload_info"]


                if _type == 'mp4' or _type == "MP4" or _type == "Mp4":
                    size = 4
                    _img = Img(
                        user_id = _user,
                        name = key,
                        yun_url = SETTING.QINIU_HOST + key,
                        fsize = fsize,
                        size = size,
                        width = vw,
                        height = vh,
                        duration = duration
                    )
                else:
                    size = 170
                    if _type == 'gif' or _type == "GIF" or _type == 'Gif':
                        size = 1
                    elif w <= h :
                        size = 2
                    elif w > h :
                        size = 3
                    _img = Img(
                        user_id = _user,
                        name = key,
                        yun_url = SETTING.QINIU_HOST + key,
                        fsize = fsize,
                        size = size,
                        width = w,
                        height = h,
                        duration = duration
                    )
                _img.save()

                print "type:",_upload_info["type"],type(_upload_info["type"])
                if _upload_info["type"] == 1: #普通用户给master传图片
                    HelpMasterAddImg(_user,_img,_upload_info)
                if _upload_info["type"] == 2: #用户上传奖励图
                    SetGatherPrizeImg()

                if _upload_info["type"] == 0: #普通用户上传图片
                    #上传的图片添加至该用户的默认目录
                    # _category = Category.objects.get( user_id = _user ,is_default = 1,id=_category_id)
                    if Category.objects.filter( user_id = _user,id=_category_id).exists() is False:
                        return HttpResponse( json.dumps({"status":"false","msg":u"用户没有此目录"}),content_type="application/json" )

                    _category = Category.objects.get( id=_category_id)
                    _rel = RelCategoryImg(category = _category,img = _img )
                    _rel.save()

                    r_img = {
                        "img_id":_img.id,
                        "yun_url":_img.yun_url, # 七牛云自动缩略图
                        "size":_img.size ,
                        "width":_img.width,
                        "height":_img.height,
                        "duration":_img.duration,
                        "category_name":_category.name,
                        "category_id":_category.id,
                    }
                    KEY_USER_HASH.pop(key)
                    return HttpResponse(json.dumps({"status":"true","img":r_img}),content_type="application/json")
            return HttpResponse(json.dumps({"status":"false","msg":u"网络出错，请重新上传"}),content_type="application/json")
        except Exception,e:
            print e
            return HttpResponse(json.dumps({"status":"false","msg":u"上传图片错误" + str(e)}),content_type="application/json")
def SetGatherPrizeImg():
    pass

def HelpMasterAddImg(user,img,upload_info):
    #图片保存到默认目录
    _category = Category.objects.get( user_id = user ,is_default = 1)
    _rel = RelCategoryImg(category = _category,img = img )
    _rel.save()

    #图片给master
    _master_uid = upload_info["master_uid"]
    _master = RelMasterImg( user_id = _master_uid,img = img )
    _master.save()
    return HttpResponse(json.dumps({"status":"true","msg":u"帮助master成功"}),content_type="application/json")