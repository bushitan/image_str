#coding:utf-8
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404
from grid.models import *

from django.views.generic import View, TemplateView, ListView, DetailView
from grid.lib.str2img import Str2Img
from grid.lib.web import Web
import datetime
import time
import json
import logging
import os
import base64
from PIL import Image,ImageDraw,ImageFont
import sys
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


#微信接口使用，图片转字符画
class WXImgToStr(BaseMixin, ListView):
    template_name = 'img_str/pc.html'

    def get_context_data(self, **kwargs):
        self.filename = self.kwargs.get('url', '')
        return super(WXImgToStr, self).get_context_data(**kwargs)
    def get_queryset(self):
        pass

    def post(self, request, *args, **kwargs):

        _img_url = self.request.POST.get("img_url", "")

        filedir = sys.path[0]+"/blog/static/img/art/"
        filename = "img_{}".format( time.strftime("%Y%m%d%H%M%S",time.localtime(time.time())))
        filestyle = ".png"
        # img_url = "http://mmbiz.qpic.cn/mmbiz/EmT9585IibD0V5dic327aVTjBFr1PgAcdzb7SDPK0Ndo3qqm26wHn6s4Qpf5TddjtpNFRrmL8CBb8Q64XuN13v4Q/0"

        _web =  Web()
        _url = r"/static/img/art/"

        _strfilename = ''
        if _web.Download_Img(filedir,filename+filestyle,_img_url ): #保存图片
            _str2img = Str2Img()
            # _url += _str2img.Grid_ByUrl(filedir,filename) # 图片转字符画
            _strfilename = _str2img.Str_ByUrl(filedir,filename+filestyle) # 图片转字符画


        mydict = {
            'url':_url,
            'filename':_strfilename
        }
        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )

class ImgToStrView(BaseMixin, ListView):
    template_name = 'img_str/pc.html'

    def get_context_data(self, **kwargs):
        return super(ImgToStrView, self).get_context_data(**kwargs)
    def get_queryset(self):
        pass

    def post(self, request, *args, **kwargs):

        data = request.POST['tx']
        # print data , 'OK1'
        if not data:
            logger.error(
                u'[UserControl]用户上传头像为空:[%s]'.format(
                    request.user.username
                )
            )
            return HttpResponse(u"上传图片并选取区域", status=500)

        _img_type = self.request.POST.get("img_type", "")
        _width = int(self.request.POST.get("width", ""))
        _height = int(self.request.POST.get("height", ""))
        _charSize = int(self.request.POST.get("char_size", ""))
        _charAscii = self.request.POST.get("char_ascii", "")
        _grid_num = int(self.request.POST.get("grid_num", ""))

        print _grid_num
        imgData = base64.b64decode(data)

        filename = "tx_100x100_{}.jpg".format(request.user.id)

        # homedir = os.path.dirname(os.path.dirname(sys.path[0]))
        # parent_path = os.path.dirname(homedir)
        filedir = sys.path[0]+"/blog/static/img/art/"
        # filedir = "art/static/img/"
        if not os.path.exists(filedir):
            os.makedirs(filedir)

        path = filedir + filename

        file = open(path, "wb+")
        file.write(imgData)
        file.flush()
        file.close()

        print _img_type
        #原画 + 方格
        if _img_type == 'normal':

            im = Image.open(path)
            print "format:",im.format, "size:",im.size, "mode:",im.mode

            WIDTH = im.size[0]
            HEIGHT = im.size[1]
            _grid = _grid_num
            _charSize = 1

            # out = im.resize((WIDTH,HEIGHT), Image.NEAREST)
            a = ImageDraw.Draw(im)

            _color = (130, 130, 130)

            if _grid > 0:
                # print _grid

                _str2img = Str2Img()
                _lines = _str2img.Process_Adapt(WIDTH,HEIGHT,_grid)

                for i in range(len(_lines)):
                    # a.line(
                    a.line([(_lines[i][0],_lines[i][1]),(_lines[i][2],_lines[i][3])],fill=_color,width=1)

                # for i in range(_grid):
                #     a.line([(0,i*HEIGHT*_charSize/_grid),(WIDTH*_charSize,i*HEIGHT*_charSize/_grid)],fill=_color,width=1)
                #     print 0,i*HEIGHT*_charSize/_grid , WIDTH*_charSize,i*HEIGHT*_charSize/_grid
                # for i in range(_grid):
                #     a.line([(i*WIDTH*_charSize/_grid,0),(i*WIDTH*_charSize/_grid,HEIGHT*_charSize)],fill=_color,width=1)

            filename = "tx_100x100_{}.jpg".format( time.strftime("%Y%m%d%H%M%S",time.localtime(time.time())))
            path = filedir + filename
            im.save(path)

            _url =   r"/static/img/art/"+filename
            mydict = {'url':_url}
            return HttpResponse(
                json.dumps(mydict),
                content_type="application/json"
            )
        #字符画 + 方格
        else:
            # 修改头像分辨率
            # im = Image.open(path)
            #
            # out = im.resize((_width, _height), Image.ANTIALIAS)
            # out.save(path)

            #Img To StrImg
            #return url
            _str2img = Str2Img()
            _url = _str2img.process(path,_width,_height,_charSize,_charAscii,_grid_num)
            mydict = {'url':_url}
            return HttpResponse(
                json.dumps(mydict),
                content_type="application/json"
            )