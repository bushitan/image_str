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


from django.test import TestCase, Client

from wx_app.views import *
# from core.tests import create_user

class ViewTest(TestCase):
    def test(self):
        response = self.client.get('/user/login')
        self.failUnlessEqual('abc', response.content)
