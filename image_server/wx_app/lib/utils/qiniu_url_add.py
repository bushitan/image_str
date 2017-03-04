# -*- coding: utf-8 -*-
from image_server.settings import (qiniu_access_key,
                                 qiniu_secret_key,
                                 qiniu_bucket_name)

import qiniu
assert qiniu_access_key and qiniu_secret_key and qiniu_bucket_name
import httplib, urllib,urllib2
# from wx_app.models import *

from wx_app.lib.filepath import FilePath
from wx_app.lib.magick import Magick
import image_server.settings as SETTING
import subprocess,json

#img_name 图片的名称（无后缀）
#img_local_path 图片的本地文件路径+文件名+后缀
def QiNiuUrlAdd(pre_url,qiniu_path,local_path,session):
	# if img_url is None:
	img_name = pre_url.split("/")[-1]
	if img_name == "":
		img_name = "1.gif"
	img_down_path = local_path + img_name

	img_down(pre_url,img_down_path) #下载文件
	img_type = img_resize(img_down_path) # 获取图片的type，重命名，改大小
	img_upload(qiniu_path,img_type,img_down_path,session) # 七牛路径 图片全名，图片上传路径


def img_down(url,down_path):
	f = urllib2.urlopen(url)
	data = f.read()
	with open(down_path, "wb") as code:
		code.write(data)

#img_local_path 不带后缀
def img_resize(img_local_path):
	print img_local_path
	magick = Magick()
	info =  magick.Identity(img_local_path)

	# img_rename_path = img_local_path +  "." + info["type"].lower()
	# _cmd = ""
	if info["type"] == "gif" :
		_cmd = u"magick convert -resize 180x240 %s %s" %(img_local_path,img_local_path)
	else:
		_cmd = u"magick convert %s %s" %(img_local_path,img_local_path)
	subprocess.check_output(_cmd, shell=True)
	return  info["type"].lower()

import ssl
USER_CATEGORY = "2" #今日斗图目录
URL  = SETTING.BASE_HOST + "upload/token/"
# URL  = "http://192.168.199.203:8000/upload/token/"
def img_upload(qiniu_path,img_type,img_path,session):
	#获取token
	# key = qiniu_path + img_name + "." + img_type
	print qiniu_path,img_type,img_path,session
	params = {
		'session': session,
		'type':img_type,
		"category_id":USER_CATEGORY,
	}
	params = urllib.urlencode(params)
	context = ssl._create_unverified_context() #跳过SSL认证~~
	ret = urllib.urlopen("%s?%s"%(URL, params),context = context)
	ret_read =  ret.read().decode("utf-8-sig")
	ret_json = json.loads( ret_read)

	#上传图片
	if ret_json["status"] == "true":
		token =  ret_json["token"]
		key = ret_json["key"]
		ret, info = qiniu.put_file(token,key, img_path)
		print ret
		if ret["status"] == "true":
			return True
	return False

if __name__ == "__main__":
	QiNiuUrlAdd(
		pre_url="http://images2015.cnblogs.com/blog/776397/201609/776397-20160913160429367-514072234.png",
		qiniu_path = "",
		local_path = r"E:\CarcerWorld\code\Python\git\image_str\image_server\wx_app\static\qiniu\\",
		session="0014oAbu1QE2Pa0lplbu1l0Bbu14oAbn1488521016.82",
	)


