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

        policy = {
            # "callbackUrl":"http://120.27.97.33/upload/token/",
            "callbackUrl":"https://www.12xiong.top/upload/token/",
            "callbackBody":"key=$(key)&hash=$(etag)&w=$(imageInfo.width)&h=$(imageInfo.height)&duration=$(avinfo.video.duration)&vw=$(avinfo.video.width)&vh=$(avinfo.video.height)",
            "callbackHost":"120.27.97.33"

            # "fsizeLimit": 1000,
            # "mimeLimit": "image/png"
        }

        token = q.upload_token(qiniu_bucket_name,key = key,policy = policy)
        # token = q.upload_token(qiniu_bucket_name,key = key)
        return token,key

    def delete(self,key):
        # try:
            #初始化Auth状态
        q = qiniu.Auth(qiniu_access_key, qiniu_secret_key)
        #初始化BucketManager
        bucket = qiniu.BucketManager(q)
        #删除bucket_name 中的文件 key  #你要测试的空间， 并且这个key在你空间中存在
        ret, info = bucket.delete(qiniu_bucket_name, key)
        print(info)
            # return True
        # except Exception as e:
        #     print 'error',e
        #     return False