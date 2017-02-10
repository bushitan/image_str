# -*- coding:utf-8 -*-

import urllib
import urllib2
import re
import os

class Filter:

    def __init__(self):
        pass
        # self.siteURL = 'http://mm.taobao.com/json/request_top_list.htm'
        # self.siteURL = 'https://github.com/composer/composer/commit/ac676f47f7bbc619678a29deae097b6b0710b799'
        # # self.siteURL = 'http://cuiqingcai.com/1001.html'
        # self.siteURL = 'http://mp.weixin.qq.com/s/4xKa1KEhXpf3ZVSGRc3phw'
        #
        # self.siteURL ="http://mp.weixin.qq.com/s?__biz=MzA5NDIzNjI1OA==&amp;mid=2455502295&amp;idx=2&amp;sn=48ba0b23e9666d87cac6d176fb071c34&amp;chksm=87fee6dab0896fccd916c460e5a96c71e9fd31072905dd09ef5d9876575a9eb7aa04b992744b&amp;mpshare=1&amp;scene=1&amp;srcid=0210DIE9DeZKH79KYf06QvCT#wechat_redirect"


    def getPage(self):
        # url = self.siteURL + "?page=" + str(pageIndex)
        url = self.siteURL
        print url
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        # return response.read().decode('gbk')
        return response.read()

    def getContents(self,siteUrl):
        self.siteURL = siteUrl
        page = self.getPage()
        # print page
        # pattern = re.compile('<div class="list-item".*?pic-word.*?<a href="(.*?)".*?<img src="(.*?)".*?<a class="lady-name.*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>',re.S)
        # pattern = re.compile('<img.*?src="(.*?\.(jpg|png))".*?/>', re.S)
        # pattern = re.compile('<img src="(.*?)".*?/>', re.S)
        pattern = re.compile('<img.*? data-src="(.*?)".*?/>', re.S)
        items = re.findall(pattern,page)
        # print items
        i = 0
        for  item in items:
            # print item
            i = i + 1
            # url =  "http:"+item
            url =  item
            name = str(i)+".gif"
            self.saveImg(url,name)
        return items
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

# spider = Filter()
# # print len(spider.imgList)
# # print spider.imgList[0].split(".")[-1]
# spider.getContents(1)


