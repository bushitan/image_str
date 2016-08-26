#coding:utf-8
from django.views.decorators.csrf import csrf_exempt
import httplib, urllib,urllib2
from django.http import HttpResponse, Http404
from grid.models import *

from django.views.generic import View, TemplateView, ListView, DetailView
from grid.lib.str2img import Str2Img
from grid.lib.web import Web
from grid.lib.qi_niu import QiNiu

import datetime
import time
import json
import logging
import os
import base64
from PIL import Image,ImageDraw,ImageFont
import sys
import image_server.settings as SETTING
from grid.lib.painter import Painter
# logger
logger = logging.getLogger(__name__)

class BaseMixin(object):
    def get_context_data(self, *args, **kwargs):

        # user = self.request.user
        # if not user.is_authenticated():
        #    kwargs['user_id'] = "none"
        # else:
        #    kwargs['user_id'] = user
        context = super(BaseMixin, self).get_context_data(**kwargs)
        return context

#
class API_PC(BaseMixin, ListView):
    template_name = 'img_str/pc.html'

    def get(self, request, *args, **kwargs):
        print "get API_PC"
        return super(API_PC, self).get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        return super(API_PC, self).get_context_data(**kwargs)
    def get_queryset(self):
        pass
    def post(self, request, *args, **kwargs):
        print "post API_PC"
        _tx = request.POST['tx']
        _imgData = base64.b64decode(_tx)

        _img_filedir = "grid/static/art/img/"
        _img_name = "{}".format(time.strftime('%Y%m%d%H%M%S'))
        _img_style = ".png"
        _img_filename = _img_name+_img_style
        _img_localpath = _img_filedir + _img_filename


        print "_img_localpath:" + _img_localpath
        #写入图片
        file = open(_img_localpath, "wb+")
        file.write(_imgData)
        file.flush()
        file.close()

        IMAGE_SERVER_HOST = 'http://120.27.97.33:91/'
        url = IMAGE_SERVER_HOST + 'grid/api/img_str/'
        data  = {  "img_url":IMAGE_SERVER_HOST + "static/art/img/"+_img_filename}

        print url,data

        req = urllib2.Request(url)
        data = urllib.urlencode(data)
        #enable cookie
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        response = opener.open(req,data)
        res = response.read()
        print 'res:',res
        return HttpResponse(res)


#图片处理api，生成字符画
#接收原图url->字符画->上传->返回字符画url
class API_ImgToStr_Temp(BaseMixin, ListView):
    template_name = 'img_str/pc.html'

    def get(self, request, *args, **kwargs):
        print request,"get"
        return super(API_ImgToStr_Temp, self).get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        return super(API_ImgToStr_Temp, self).get_context_data(**kwargs)
    def get_queryset(self):
        pass
    def post(self, request, *args, **kwargs):
        print 'OK API_ImgToStr_Temp'
        _img_url = self.request.POST.get("img_url", "")
        #图片路径
        _img_filedir = "grid/static/art/img/"
        _img_name = "{}".format(time.strftime('%Y%m%d%H%M%S'))
        _img_style = ".png"
        _img_filename = _img_name+_img_style
        _img_localpath = _img_filedir + _img_filename

        _str_filedir = "grid/static/art/str/"
        _str_name = "{}".format( time.strftime("%Y%m%d%H%M%S",time.localtime(time.time())))
        _str_style = ".png"
        _str_filename = _str_name + _str_style
        _str_localpath = _str_filedir + _str_filename + _str_style

        _sketch_filedir = "grid/static/art/sketch/"
        _sketch_name = "{}".format( time.strftime("%Y%m%d%H%M%S",time.localtime(time.time())))
        _sketch_style = ".png"
        _sketch_filename = _sketch_name + _sketch_style
        _sketch_localpath =  _sketch_filedir +  _sketch_filename + _sketch_style

        _qiniu_img_path = 'img/'
        _qiniu_str_path = 'str/'
        _qiniu_grid_path = 'grid/'
        _qiniu_sketch_path = 'sketch/'

        _web = Web()
        _str2img = Str2Img()
        _qiniu = QiNiu()

        print "IN down"
         #保存图片到本地
        if _web.Download_Img(_img_filedir,_img_filename,_img_url ): #保存图片
            # _str_filename = _str2img.Str_ByUrl(_img_filedir,_img_filename,_str_filedir) # 字符画存储路径，原图路径，
            print _img_localpath , _str_filedir
            if Painter.ImgCharLine(_img_localpath,_str_localpath,_sketch_localpath): #图片、组孵化、线稿
                #上传图片
                _img_name = _qiniu.put(_qiniu_img_path,_img_filename,_img_localpath)#上传原图
                _str_name = _qiniu.put(_qiniu_str_path,_str_filename,_str_localpath)#上传字符画
                _sketch_name = _qiniu.put(_qiniu_sketch_path,_sketch_filename,_sketch_localpath)

                _img_url = SETTING.QINIU_HOST + _img_name
                _str_url = SETTING.QINIU_HOST + _str_name
                _sketch_url = SETTING.QINIU_HOST + _sketch_name

                mydict = {
                    'img_url':_img_url,
                    'str_url':_str_url,
                    'sketch_url':_sketch_url
                }
                # mydict = {
                #     'img_url':_img_name,
                #     # 'str_url':_str_name,
                #     # 'sketch_url':_sketch_name
                # }
                return HttpResponse(
                    json.dumps(mydict),
                    content_type="application/json"
                )
        return HttpResponse(u"下载微信图片失败")


class API_Game_ActiveCircle(BaseMixin, ListView):
    # template_name = 'img_str/pc.html'

    # def get(self, request, *args, **kwargs):
    #     print request,"get"
    #     return super(API_Game_ActiveCircle, self).get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        return super(API_Game_ActiveCircle, self).get_context_data(**kwargs)
    def get_queryset(self):
        pass
    def post(self, request, *args, **kwargs):
        # print 'OK temp'
        _img_url = self.request.POST.get("img_url", "")
        #图片路径
        _img_filedir = "grid/static/art/img/"
        _img_name = "{}".format(time.strftime('%Y%m%d%H%M%S'))
        _img_style = ".png"
        _img_filename = _img_name+_img_style
        _img_localpath = _img_filedir + _img_filename

        _str_filedir = "grid/static/art/str/"
        _str_filename = "{}".format( time.strftime("%Y%m%d%H%M%S",time.localtime(time.time())))
        filestyle = ".png"
        _str_localpath = _str_filedir + _str_filename + filestyle

        _qiniu_img_path = 'img/'
        _qiniu_str_path = 'str/'
        _qiniu_grid_path = 'grid/'

        _web = Web()
        # _str2img = Str2Img()
        _qiniu = QiNiu()

         #保存图片到本地


        #游戏使用
        if _web.Download_Img(_img_filedir,_img_filename,_img_url ): #保存图片
            # _str_filename = _str2img.Str_ByUrl(_img_filedir,_img_filename,_str_filedir) # 字符画存储路径，原图路径，
            print _img_localpath , _str_filedir

            mydict = Painter.Game_ActiveCircle(_img_localpath,_str_localpath)#图片转字符画成功,获取游戏数据
            #上传图片
            _img_name = _qiniu.put(_qiniu_img_path,_img_filename,_img_localpath)#上传原图
            _str_name = _qiniu.put(_qiniu_str_path,_str_filename,_str_localpath)#上传字符画
            # _str_name = 'tt'
            _img_url = SETTING.QINIU_HOST + _img_name
            _str_url = SETTING.QINIU_HOST + _str_name

            mydict['img_url'] =_img_url
            mydict['str_url'] =_str_url

            return HttpResponse(
                json.dumps(mydict),
                content_type="application/json"
            )
        return HttpResponse(u"下载微信图片失败")
#图片处理api，生成字符画
#接收原图url->字符画->上传->返回字符画url
# class API_ImgToStr(BaseMixin, ListView):
#     template_name = 'img_str/pc.html'
#
#     def get(self, request, *args, **kwargs):
#         print request,"get"
#         return super(API_ImgToStr, self).get(request, *args, **kwargs)
#     def get_context_data(self, **kwargs):
#         return super(API_ImgToStr, self).get_context_data(**kwargs)
#     def get_queryset(self):
#         pass
#     def post(self, request, *args, **kwargs):
#         print 'OK'
#         _img_url = self.request.POST.get("img_url", "")
#         print _img_url
#         #图片路径
#         _img_filedir = "grid/static/art/img/"
#         _img_name = "{}".format(time.strftime('%Y%m%d%H%M%S'))
#         _img_style = ".png"
#         _img_filename = _img_name+_img_style
#         _img_localpath = _img_filedir + _img_filename
#
#         _str_filedir = "grid/static/art/str/"
#
#
#         _qiniu_img_path = 'img/'
#         _qiniu_str_path = 'str/'
#         _qiniu_grid_path = 'grid/'
#
#         _web = Web()
#         _str2img = Str2Img()
#         _qiniu = QiNiu()
#
#          #保存图片到本地
#         if _web.Download_Img(_img_filedir,_img_filename,_img_url ): #保存图片
#             print 'download is success'
#             # print _str_filedir,_img_filename,_str_filedir+_img_filename
#             _str_filename = _str2img.Str_ByUrl(_img_filedir,_img_filename,_str_filedir) # 字符画存储路径，原图路径，
#             print _str_filename
#             _str_localpath = _str_filedir + _str_filename
#
#
#             _img_name = _qiniu.put(_qiniu_img_path,_img_filename,_img_localpath)#上传原图
#             _str_name = _qiniu.put(_qiniu_str_path,_str_filename,_str_localpath)#上传字符画
#
#             _img_url = SETTING.QINIU_HOST + _img_name
#             _str_url = SETTING.QINIU_HOST + _str_name
#
#             mydict = {
#                 'img_url':_img_url,
#                 'str_url':_str_url
#             }
#             return HttpResponse(
#                 json.dumps(mydict),
#                 content_type="application/json"
#             )
#         return HttpResponse(u"下载微信图片失败")
#
# #微信接口使用，图片转字符画
# class WXImgToStr(BaseMixin, ListView):
#     template_name = 'img_str/pc.html'
#
#     def get_context_data(self, **kwargs):
#         self.filename = self.kwargs.get('url', '')
#         return super(WXImgToStr, self).get_context_data(**kwargs)
#     def get_queryset(self):
#         pass
#
#     def post(self, request, *args, **kwargs):
#
#         _img_url = self.request.POST.get("img_url", "")
#
#         filedir = sys.path[0]+"/grid/static/img/art/"
#         filename = "img_{}".format( time.strftime("%Y%m%d%H%M%S",time.localtime(time.time())))
#         filestyle = ".png"
#         # img_url = "http://mmbiz.qpic.cn/mmbiz/EmT9585IibD0V5dic327aVTjBFr1PgAcdzb7SDPK0Ndo3qqm26wHn6s4Qpf5TddjtpNFRrmL8CBb8Q64XuN13v4Q/0"
#
#         _web =  Web()
#         _url = r"/static/img/art/"
#
#         _strfilename = ''
#         if _web.Download_Img(filedir,filename+filestyle,_img_url ): #保存图片
#             _str2img = Str2Img()
#             # _url += _str2img.Grid_ByUrl(filedir,filename) # 图片转字符画
#             _strfilename = _str2img.Str_ByUrl(filedir,filename+filestyle) # 图片转字符画
#
#
#         mydict = {
#             'url':_url,
#             'filename':_strfilename
#         }
#         return HttpResponse(
#             json.dumps(mydict),
#             content_type="application/json"
#         )
#
# class ImgToStrView(BaseMixin, ListView):
#     template_name = 'img_str/pc.html'
#
#     def get_context_data(self, **kwargs):
#         return super(ImgToStrView, self).get_context_data(**kwargs)
#     def get_queryset(self):
#         pass
#
#     def post(self, request, *args, **kwargs):
#
#         data = request.POST['tx']
#         # print data , 'OK1'
#         if not data:
#             logger.error(
#                 u'[UserControl]用户上传头像为空:[%s]'.format(
#                     request.user.username
#                 )
#             )
#             return HttpResponse(u"上传图片并选取区域", status=500)
#
#         _img_type = self.request.POST.get("img_type", "")
#         _width = int(self.request.POST.get("width", ""))
#         _height = int(self.request.POST.get("height", ""))
#         _charSize = int(self.request.POST.get("char_size", ""))
#         _charAscii = self.request.POST.get("char_ascii", "")
#         _grid_num = int(self.request.POST.get("grid_num", ""))
#
#         print _grid_num
#         imgData = base64.b64decode(data)
#
#         filename = "tx_100x100_{}.jpg".format(request.user.id)
#
#         # homedir = os.path.dirname(os.path.dirname(sys.path[0]))
#         # parent_path = os.path.dirname(homedir)
#         filedir = sys.path[0]+"/blog/static/img/art/"
#         # filedir = "art/static/img/"
#         if not os.path.exists(filedir):
#             os.makedirs(filedir)
#
#         path = filedir + filename
#
#         file = open(path, "wb+")
#         file.write(imgData)
#         file.flush()
#         file.close()
#
#         print _img_type
#         #原画 + 方格
#         if _img_type == 'normal':
#
#             im = Image.open(path)
#             print "format:",im.format, "size:",im.size, "mode:",im.mode
#
#             WIDTH = im.size[0]
#             HEIGHT = im.size[1]
#             _grid = _grid_num
#             _charSize = 1
#
#             # out = im.resize((WIDTH,HEIGHT), Image.NEAREST)
#             a = ImageDraw.Draw(im)
#
#             _color = (130, 130, 130)
#
#             if _grid > 0:
#                 # print _grid
#
#                 _str2img = Str2Img()
#                 _lines = _str2img.Process_Adapt(WIDTH,HEIGHT,_grid)
#
#                 for i in range(len(_lines)):
#                     # a.line(
#                     a.line([(_lines[i][0],_lines[i][1]),(_lines[i][2],_lines[i][3])],fill=_color,width=1)
#
#                 # for i in range(_grid):
#                 #     a.line([(0,i*HEIGHT*_charSize/_grid),(WIDTH*_charSize,i*HEIGHT*_charSize/_grid)],fill=_color,width=1)
#                 #     print 0,i*HEIGHT*_charSize/_grid , WIDTH*_charSize,i*HEIGHT*_charSize/_grid
#                 # for i in range(_grid):
#                 #     a.line([(i*WIDTH*_charSize/_grid,0),(i*WIDTH*_charSize/_grid,HEIGHT*_charSize)],fill=_color,width=1)
#
#             filename = "tx_100x100_{}.jpg".format( time.strftime("%Y%m%d%H%M%S",time.localtime(time.time())))
#             path = filedir + filename
#             im.save(path)
#
#             _url =   r"/static/img/art/"+filename
#             mydict = {'url':_url}
#             return HttpResponse(
#                 json.dumps(mydict),
#                 content_type="application/json"
#             )
#         #字符画 + 方格
#         else:
#             # 修改头像分辨率
#             # im = Image.open(path)
#             #
#             # out = im.resize((_width, _height), Image.ANTIALIAS)
#             # out.save(path)
#
#             #Img To StrImg
#             #return url
#             _str2img = Str2Img()
#             _url = _str2img.process(path,_width,_height,_charSize,_charAscii,_grid_num)
#             mydict = {'url':_url}
#             return HttpResponse(
#                 json.dumps(mydict),
#                 content_type="application/json"
#             )