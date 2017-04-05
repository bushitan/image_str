#coding=utf8
import ssl,urllib,time

#获取token
URL_HOST =  "https://www.12xiong.top/"
# URL_HOST =  "http://192.168.199.203:8000/"
URL_AUTO_CREATE_TIME  = URL_HOST + "tag/random/"
SLEEP_TIME = 3600
def AUTO():
	context = ssl._create_unverified_context() #跳过SSL认证~~
	ret = urllib.urlopen("%s"%(URL_AUTO_CREATE_TIME),context = context)
	ret_read =  ret.read().decode("utf-8-sig")
	print ret_read

while(True):
	print u'自动将今日斗图沉底图片置顶'
	time.sleep( SLEEP_TIME )
	AUTO()
