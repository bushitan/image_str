# -*- coding:utf-8 -*-

import urllib
import urllib2
import re
import os

class Spider:

    def __init__(self):
        # self.siteURL = 'http://mm.taobao.com/json/request_top_list.htm'
        self.siteURL = 'https://github.com/composer/composer/commit/ac676f47f7bbc619678a29deae097b6b0710b799'
        # self.siteURL = 'http://cuiqingcai.com/1001.html'
        self.siteURL = 'http://mp.weixin.qq.com/s/4xKa1KEhXpf3ZVSGRc3phw'

    def getPage(self,pageIndex):
        # url = self.siteURL + "?page=" + str(pageIndex)
        url = self.siteURL
        print url
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        # return response.read().decode('gbk')
        return response.read()

    def getContents(self,pageIndex):
        page = self.getPage(pageIndex)
        # print page
        # pattern = re.compile('<div class="list-item".*?pic-word.*?<a href="(.*?)".*?<img src="(.*?)".*?<a class="lady-name.*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>',re.S)
        # pattern = re.compile('<img.*?src="(.*?\.(jpg|png))".*?/>', re.S)
        # pattern = re.compile('<img src="(.*?)".*?/>', re.S)
        pattern = re.compile('<img.*? data-src="(.*?)".*?/>', re.S)
        items = re.findall(pattern,page)
        print items
        i = 0
        for  item in items:
            print item
            i = i + 1
            # url =  "http:"+item
            url =  item
            name = str(i)+".jpg"
            self.saveImg(url,name)
    #传入图片地址，文件名，保存单张图片
    def saveImg(self,imageURL,fileName):
         u = urllib.urlopen(imageURL)
         data = u.read()
         f = open(fileName, 'wb')
         f.write(data)
         f.close()

    #创建新目录
    def mkdir(self,path):
        path = path.strip()
        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists=os.path.exists(path)
        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(path)
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            return False

spider = Spider()
# print len(spider.imgList)
# print spider.imgList[0].split(".")[-1]
spider.getContents(1)


# i=0
# for  item in spider.imgList:
#     # print item
#     i = i + 1
#     if i>10:
#         # continue
#     # url =  "http:"+item
#         print item
#         url =  item
#         name = item.split(".")[-1]
#         # name = str(i)+"."+ item.split(".")[-1]
#         if name == "gif" or name == "GIF" or name == "jpg" or name == "png" or name == "jpeg" :
#             pass
#             name = str(i)+"."+ item.split(".")[-1]
#         else:
#             name = str(i)+".gif"
#         print name
#         spider.saveImg(url,name)
# spider.saveImg("http://gtd.alicdn.com/sns_logo/i6/TB1EjxDKXXXXXXhaXXXSutbFXXX.jpg_60x60.jpg","1.jpg")