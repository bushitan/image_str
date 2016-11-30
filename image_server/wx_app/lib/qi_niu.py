# -*- coding: utf-8 -*-
from django.http import HttpResponse
# import qiniu
import qiniu
from image_server.settings import (qiniu_access_key,
                                 qiniu_secret_key,
                                 qiniu_bucket_name)

assert qiniu_access_key and qiniu_secret_key and qiniu_bucket_name
import sys
import os
import logging
# logger
logger = logging.getLogger(__name__)

class QiNiu():
    # 上传头像到七牛,返回图片存储名字
    def put(self,qiniu_path,filename,path):
        try:

            print 1
            q = qiniu.Auth(qiniu_access_key, qiniu_secret_key)

            key = qiniu_path + filename
            localfile = path

            # mime_type = "text/plain"
            mime_type = "image/png"
            params = {'x:a': 'a'}

            print params
            token = q.upload_token(qiniu_bucket_name, key)
            ret, info = qiniu.put_file(token, key, localfile,
                                       mime_type=mime_type, check_crc=True)
            print info
            # 验证上传是否错误
            if ret['key'] != key or ret['hash'] != qiniu.etag(localfile):
                logger.error(
                    u'[UserControl]上传头像错误：[{}]'.format(
                        'test'
                    )
                )
                return HttpResponse(u"上传头像错误", status=500)

            return True

        except Exception as e:
            # request.user.img = "/static/tx/"+filename
            # request.user.save()
            print 'error',e
            # 验证上传是否错误
            if not os.path.exists(path):
                logger.error(
                    u'[UserControl]用户上传头像出错:[{}]'.format(
                        'test'
                        # request.user.username
                    )
                )
                return HttpResponse(u"上传头像错误", status=500)

            return HttpResponse(u"上传头像成功!\n(注意有10分钟缓存)")
    def getToken(self,qiniu_path,filename,path):
        q = qiniu.Auth(qiniu_access_key, qiniu_secret_key)

        key = qiniu_path + filename
        localfile = path

        # mime_type = "text/plain"
        mime_type = "image/png"
        params = {'x:a': 'a'}

        token = q.upload_token(qiniu_bucket_name, key)
        return token,key
