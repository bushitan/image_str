#-*- coding: utf-8 -*-
# # import httplib, urllib,urllib2
# # from lib.magick import Magick
# #
# # import os
# # from wx_app.lib.filepath import FilePath
# # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # FILE_PATH = FilePath(BASE_DIR)
# #
# # import json
# # from PIL import Image
# #
# # if __name__ == '__main__':
# #
# #     #http://127.0.0.1:8000/art/wx_img_str
# #     httpClient = None
# #     try:
# #         #下载文件
# #         # url = "http://7xsark.com1.z0.glb.clouddn.com/12_20161124144609.mp4"
# #         # name = str(url).split("/")[-1]
# #         # img_down_path = FILE_PATH.Down(name)["local_path"]
# #         # f = urllib2.urlopen(url)
# #         # data = f.read()
# #         # with open(img_down_path, "wb") as code:
# #         #     code.write(data)
# #         #
# #         # #视频转换
# #         # img_type = "gif"
# #         # user_id = 59
# #         # img_up_path = FILE_PATH.Up(img_type,user_id) #按用户id命名图片
# #         # # print
# #         # magick = Magick(img_up_path["local_path"])
# #         # magick.Video2Gif(0,6,img_down_path)
# #         #
# #         #
# #         # url = 'https://www.12xiong.top/wx_app/img/query/'
# #         #
# #         # data  = {  "img_url":"http://7xsark.com1.z0.glb.clouddn.com/0_20161025165325.gif"}
# #         # data  = {  "img_url":"http://7xsark.com1.z0.glb.clouddn.com/yuan.gif?imageMogr2/thumbnail/170x240"}
# #         #
# #         # data = {
# #         #     'uid': 10 ,
# #         #     'category_id': 'null',
# #         # }
# #
# #         # http_str = 'http://127.0.0.1:12345/apps/' + serviceLine + '/clusters/' + clusterName
# #         url = "'http://120.27.97.33/upload/token/"
# #         # url = http_str + '/machine_info'
# #         # req = urllib2.Request(url) # url 转换成发起get 请求的url
# #         # result = urllib2.urlopen(req) # 发起GET http服务
# #
# #
# #         url = "http://120.27.97.33/upload/token/"
# #         # url = "http://127.0.0.1:8000/upload/token/"
# #
# #         data  = {  "img_url":"http://7xsark.com1.z0.glb.clouddn.com/0_20161025165325.gif"}
# #         req = urllib2.Request(url)
# #         data = urllib.urlencode(data)
# #         #enable cookie
# #         opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
# #         response = opener.open(req,data)
# #         res = response.read()
# #         print res
# #         # obj = json.loads(res)
# #         # print obj['img_url']
# #         # print obj['str_url']
# #     except Exception, e:
# #         print e
# #     finally:
# #         if httpClient:
# #             httpClient.close()
#
# # coding:gbk
# import time
# import urllib2
# import threading
# from Queue import Queue
# from time import sleep
#
# # 性能测试页面
# # PERF_TEST_URL = "http://127.0.0.1:8000/category/query/?session=ds9"
# PERF_TEST_URL = "https://www.12xiong.top/category/query/?session=ds9"
#
# # 配置:压力测试
# #THREAD_NUM = 10            # 并发线程总数
# #ONE_WORKER_NUM = 500       # 每个线程的循环次数
# #LOOP_SLEEP = 0.01      # 每次请求时间间隔(秒)
#
# # 配置:模拟运行状态
# THREAD_NUM = 500        # 并发线程总数
# ONE_WORKER_NUM = 10      # 每个线程的循环次数
# LOOP_SLEEP = 0.5        # 每次请求时间间隔(秒)
#
#
#
# # 出错数
# ERROR_NUM = 0
#
#
# #具体的处理函数，负责处理单个任务
# def doWork(index):
#     t = threading.currentThread()
#     #print "["+t.name+" "+str(index)+"] "+PERF_TEST_URL
#
#     try:
#         html = urllib2.urlopen(PERF_TEST_URL).read()
#     except urllib2.URLError, e:
#         print "["+t.name+" "+str(index)+"] "
#         print e
#         global ERROR_NUM
#         ERROR_NUM += 1
#
#
# #这个是工作进程，www.linuxidc.com负责不断从队列取数据并处理
# def working():
#     t = threading.currentThread()
#     print "["+t.name+"] Sub Thread Begin"
#
#     i = 0
#     while i < ONE_WORKER_NUM:
#         i += 1
#         doWork(i)
#         sleep(LOOP_SLEEP)
#
#     print "["+t.name+"] Sub Thread End"
#
#
# def main():
#     #doWork(0)
#     #return
#
#     t1 = time.time()
#
#     Threads = []
#
#     # 创建线程
#     for i in range(THREAD_NUM):
#         t = threading.Thread(target=working, name="T"+str(i))
#         t.setDaemon(True)
#         Threads.append(t)
#
#     for t in Threads:
#         t.start()
#
#     for t in Threads:
#         t.join()
#
#     print "main thread end"
#
#     t2 = time.time()
#     print "========================================"
#     print "URL:", PERF_TEST_URL
#     print "任务数量:", THREAD_NUM, "*", ONE_WORKER_NUM, "=", THREAD_NUM*ONE_WORKER_NUM
#     print "总耗时(秒):", t2-t1
#     print "每次请求耗时(秒):", (t2-t1) / (THREAD_NUM*ONE_WORKER_NUM)
#     print "每秒承载请求数:", 1 / ((t2-t1) / (THREAD_NUM*ONE_WORKER_NUM))
#     print "错误数量:", ERROR_NUM
# # 任务数量: 100 * 10 = 1000
# # 总耗时(秒): 45.9719998837
# # 每次请求耗时(秒): 0.0459719998837
# # 每秒承载请求数: 21.7523710635
# # 错误数量: 0
#
# # 任务数量: 100 * 10 = 1000
# # 总耗时(秒): 15.8619999886
# # 每次请求耗时(秒): 0.0158619999886
# # 每秒承载请求数: 63.0437524096
# # 错误数量: 82
# import  image_server.settings as SETTINGS
# if __name__ == "__main__":
#     # main()
#     dir =  SETTINGS.BASE_DIR + "/cache_today.txt"
#     fileHandler = open(dir,'a+')   #或者调用open()函数
#     # fileHandler.write("\r\n")
#     fileHandler.seek(0)
#     contents = fileHandler.read()
#     print contents
#     fileHandler.close()


# from django.test import TestCase, Client
#
# from wx_app.views import *
# from core.tests import create_user

# class ViewTest(TestCase):
#     def test(self):
#         response = self.client.get('/user/login')
#         self.failUnlessEqual('abc', response.content)
# import os,sys
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
#
# from django.core.management import execute_from_command_line
#
# load_env()
# execute_from_command_line(sys.argv)
# from  wx_app.lib.utils.wx_login import WxUserLogin
# if __name__ == "__main__":
#
#
# 	code = "051rqeXE0IKuwh2A9TZE0XFnXE0rqeXR"
# 	session = "051XgwH40A6C6H1U2dJ40G1zH40XgwHV1488348914.3"
# 	WxUserLogin(code,session)

# from django.conf import settings
# settings.configure()
# from wx_app.models import *
# import os
# import django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoHelloworld.settings");
# django.setup()  #添加的代码
# _list = Category.objects.filter( user_id = 2)
# # print _list
# _category_list = []
# for c in _list:
# 	if c.parent_id is None:
# 		_parent_id = None
# 	else:
# 		_parent_id = c.parent_id.id
# 	_category_list.append({
# 		"category_id":c.id,
# 		"name":c.name,
# 		"parent_id": _parent_id,
# 		"sn":c.sn,
# 	})
#
# #排序
# _category_list.sort(lambda x,y: cmp(x['sn'], y['sn']))
# _category_list = sorted(_category_list, key=lambda x:x['sn'])
#
# print _category_list







# str = '''
# [{
#         title:"康夫电吹风机家用大功率2300W发廊理发店学生电吹风筒静音冷热风",
#         img:"../../images/tb_img.jpg",
#         price:"185",
#         discount_price:"168",
#         sale:"18511",
#         store_url:"https://s.click.taobao.com/bcZUHow",
#         store_qr:"http://gqrcode.alicdn.com/img?type=hv&text=https%3A%2F%2Fs.click.taobao.com%2FbcZUHow%3Faf%3D3&h=300&w=300",
#     },{
#         title:"康夫电吹风机家用大功率2300W发廊理发店学生电吹风筒静音冷热风",
#         img:"../../images/tb_img.jpg",
#         price:"185",
#         discount_price:"168",
#         sale:"18511",
#         store_url:"https://s.click.taobao.com/bcZUHow",
#         store_qr:"http://gqrcode.alicdn.com/img?type=hv&text=https%3A%2F%2Fs.click.taobao.com%2FbcZUHow%3Faf%3D3&h=300&w=300",
#     }]
# '''
# str = '''{title:"康夫电吹风机家用大功率2300W发廊理发店学生电吹风筒静音冷热风",img:"../../images/tb_img.jpg",price:"185",discount_price:"168",sale:"18511",store_url:"https://s.click.taobao.com/bcZUHow",store_qr:"http://gqrcode.alicdn.com/img?type=hv&text=https%3A%2F%2Fs.click.taobao.com%2FbcZUHow%3Faf%3D3&h=300&w=300",}'''
# # str="{'title':'1'}"
# str = '''[{
#         "title":"康夫电吹风机家用大功率2300W发廊理发店学生电吹风筒静音冷热风",
#         "img":"../../images/tb_img.jpg",
#         "price":"185",
#         "discount_price":"168",
#         "sale":"18511",
#         "store_url":"https://s.click.taobao.com/bcZUHow",
#         "store_qr":"http://gqrcode.alicdn.com/img?type=hv&text=https%3A%2F%2Fs.click.taobao.com%2FbcZUHow%3Faf%3D3&h=300&w=300",
#     },{
#         "title":"康夫电吹风机家用大功率2300W发廊理发店学生电吹风筒静音冷热风",
#         "img":"../../images/tb_img.jpg",
#         "price":"185",
#         "discount_price":"168",
#         "sale":"18511",
#         "store_url":"https://s.click.taobao.com/bcZUHow",
#         "store_qr":"http://gqrcode.alicdn.com/img?type=hv&text=https%3A%2F%2Fs.click.taobao.com%2FbcZUHow%3Faf%3D3&h=300&w=300",
#     }]'''
# # print str
# import json
#
# decoded = eval(str)
# print decoded
#
#

# # GET , POST 测试
# import urllib2,json
#
# # url = 'http://api.weixin.qq.com/wxa/getwxacodeunlimit?access_token=%s' % ( TIME_OUT['ACCESS_TOKEN'])
# url = "http://192.168.199.203:8001/qiniu/upload/"
#
# session = "021I0xhq0fLEBq1Eyyjq0qrlhq0I0xhH1496302722.89"
# get_url = url + "?session=%s&type=gif" %( session )
# req = urllib2.Request(get_url)
# opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
# response = opener.open(req)
# print response.read()
#
# data = {
#     'key': '1.gif',
#     'hash': "",
#     'w': 200,
#     'h': 200,
#     'duration': 10,
#     'fsize': 512,
#     'vw': 0,
#     'vh': 0,
# }
# headers = {'Content-Type': 'application/json'}
# request = urllib2.Request(url = url,  headers=headers, data=json.dumps(data))
# response = urllib2.urlopen(request)
# print response.read()

# 打开浏览器

#!/usr/bin/env python
#-*- coding:UTF-8 -*-
import sys
# import webbrowser
# import base64
# logo = 'aHR0cDovL3d4LnFsb2dvLmNuL21tb3Blbi92aV8zMi9RMGo0VHdHVGZUS1ZqT3VjbzM5aWF5QnlKRGFndmRIWGoxSnNyNmpHZUYwYUhrV015Z3ZWeXBtU2RFeVZtWmhydWFaZU82YTdsZTU0ZklYZnl1cGliaWNkZy8w'
# qr = 'aHR0cDovL2ltZy4xMnhpb25nLnRvcC9tYXN0ZXIvMS5qcGc'
# title = '6buE5Zu-57qi5Zu-55qu5aWl5Yip5aWl55qE'
# # prize_url = 'aHR0cDovL2ltYWdlLjEyeGlvbmcudG9wLzFfMjAxNzA2MDYxMDM2MzEuanBn'
# prize_url = 'aHR0cDovL2ltZy4xMnhpb25nLnRvcC8xMDExXzIwMTcwMjE0MjIxMTAxLmpwZw=='
# # prize_url = "aHR0cDovL2ltZy4xMnhpb25nLnRvcC8xMl8yMDE2MTIwMzE1NTI0OC5naWY_aW1hZ2VNb2dyMi90aHVtYm5haWwvMTcweDI0MC9mb3JtYXQvanBn"
#
#
# want1 = '5oOz6KaB'
# num = 'Tk86MTEyNDM="'
# mark = '6L-Z5piv56aP5Yip'
#
#
# water_5 = 'http://img.12xiong.top/help_tie_bg4.jpg?watermark/3/'  \
#   + 'image/' + logo + '/dissolve/100/gravity/North/dx/-40/dy/105/ws/0.15/'\
#   + 'text/' + want1 + '/font/5b6u6L2v6ZuF6buR/fontsize/500/fill/YmxhY2s=/dissolve/85/gravity/North/dx/35/dy/115/'\
#   + 'text/' + title + '/font/5b6u6L2v6ZuF6buR/fontsize/500/fill/YmxhY2s=/dissolve/85/gravity/North/dx/0/dy/165/'\
#   + 'image/' + prize_url + '/dissolve/15/gravity/Center/dx/0/dy/0/ws/0.2/'\
#   + 'text/' + mark + '/font/5b6u6L2v6ZuF6buR/fontsize/300/fill/cmVk/dissolve/85/gravity/Center/dx/0/dy/0/'\
#   + 'image/' + qr + '/dissolve/100/gravity/South/dx/0/dy/20/ws/0.45/'\
#   + 'text/' + num + '/font/5b6u6L2v6ZuF6buR/fontsize/300/fill/cmVk/dissolve/85/gravity/South/dx/0/dy/0/'\
#
# webbrowser.open(water_5)

# http://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKVjOuco39iayByJDagvdHXj1Jsr6jGeF0aHkWMygvVypmSdEyVmZhruaZeO6a7le54fIXfyupibicdg/0
#http://image.12xiong.top/1_20170606103631.jpg



# from django.conf import settings
# settings.configure()
from wx_app.models import *
import json

# import os
# os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

_story_id = 1
_step_current = "1,3"
# _tree = Story.objects.get(id = _story_id ).tree
# _tree_json =  json.loads(_tree)           #剧情树转json
#
# # print _current_art_id
# if _step_current == "":                        #从故事列表进入，步骤为空
#     _current_art_id = _tree_json.keys()[0] #获取当前文章的id
#     _art_list = [_current_art_id]           #第一步为用户已经走的路
# else:
#     _art_list = _step_current.split(',')
#     _current_art_id = _art_list[-1]         #最新的步数为当前浏览步数
# # print _art_list
# _step_next = {}     #设置下一步信息你
# temp = _tree_json
# for item in _art_list: #遍历步骤列表
#     temp=temp[item]
#     if item == _art_list[-1]: #根据步骤，获取当前步数的son
#         key_list = ["right_id", "right_name","left_id","left_name"]
#         for k in key_list:    #将son的左右数据，依次存入_step_next
#             if temp.has_key(k):
#                 _step_next[k] = temp[k]
#
# a = Article.objects.get(id = _current_art_id )  #当前步数对应的文章
#
# _dict = {
#     "status":"true",
#     "swiper": a.swiper.replace('\r\n','').split(",") , #轮播图
#     "title":a.title,
#     "content":a.content,
#     "step_current":','.join(_art_list),
#     "step_next":_step_next,
# }
#
# print _dict





# print s.name, json.loads(s.tree)
# t =  json.loads(s.tree)
# _story =  '''{
# 	"1":
# 	{
# 	    "right_id":"2",
# 	    "right_name":"右边的",
# 	    "left_id":"3",
# 	    "left_name":"左边的",
#
#         "2":
#         {
#
#         },
#         "3":
#         {
#
#         }
# 	}
# }'''



