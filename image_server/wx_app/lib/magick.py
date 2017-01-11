#--coding:utf-8--
from moviepy.editor import *
import subprocess
import logging
import os
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
class Magick():
    save_url = ""
    def __init__(self,save_url=""):
        self.save_url = save_url
        pass

    #图片打水印  simhei.ttf 字体要在同一文件夹下
    # jpg/png 能打 文字/图片/gif水印
    # gif 能打文字水印
    def AddWatermark(self,img,txt_file = "t.txt"):

        #把原图copy成save，字体在原图更改
        _cmd = u"magick %s %s " % (img,self.save_url )
        subprocess.check_output(_cmd, shell=True)

        _resouces_path = BASE_DIR + "/static/magick/resouces/"
        _txt_file = _resouces_path + txt_file
        # _img = "pre1.gif"
        _size = "-pointsize 12"

        _font = "-font %ssimhei.ttf" % (_resouces_path)
        # _fill = "-fill white -weight bolder"
        _fill = "-fill white -undercolor #00000080 -weight bolder"
        offsetX = 0
        offsetY = 0
        # _cmd = u"magick  mogrify %s %s %s  -annotate 0x0+%s+%s @%s %s" % (_font,_size,_fill,offsetX,offsetY,_txt_file,self.save_url)

        #右下角水印
        _cmd = u"magick  mogrify %s %s %s  -gravity southeast -geometry +0+0  -annotate 0x0+%s+%s @%s %s" % (_font,_size,_fill,offsetX,offsetY,_txt_file,self.save_url)
        subprocess.check_output(_cmd, shell=True)
        return

    #视频 -> gif
    # 视频要6s以内
    # fps:10 ，




    # 两张图片拼Gif
    # 以第一张图片Wie模板
    # 固定128的大小
    def Join(self,imgList=[],save_path=""):
        _out_range = 180
        img1_src = imgList[0]
        img2_src = imgList[1]
        save_url = save_path

        # img1_pre_src = BASE_DIR + "/static/magick/temp/pre1.gif"
        # img2_pre_src = BASE_DIR + "/static/magick/temp/pre2.gif"
        # bg_pre_src = BASE_DIR + "/static/magick/temp/pre_black.jpg"

        #按_out_range ，按固定比例压缩图片
        _cmd = u"magick convert -resize %sx%s %s %s" % (_out_range,_out_range,img1_src,img1_src)
        subprocess.check_output(_cmd, shell=True)

        #解析第一张图片压缩后数据,以此为模板
        img1 = self.Identity(img1_src)
        _out_w = float(img1['width'])
        _out_h = float(img1['height'])
        _out_r = _out_h/_out_w

        #按照图1的比例，压缩图2
        _cmd = u"magick convert -resize %sx%s %s %s" % (_out_w,_out_h,img2_src,img2_src)
        subprocess.check_output(_cmd, shell=True)

        #解析图二压缩后数据，
        img2 = self.Identity(img2_src)
        img2_w = float(img2['width'])
        img2_h = float(img2['height'])

        #第2张图片偏移量
        offsetY = int(( _out_h - img2_h ) /2)
        offsetX = int(( _out_w - img2_w ) /2)
        print _out_h,_out_w
        print img2_h,img2_w

        #图片2加黑边
        _cmd = u'magick convert -border  %sx%s -bordercolor "#000000"  %s %s' % (offsetX,offsetY,img2_src,img2_src)
        subprocess.check_output(_cmd, shell=True)


        #按照图1的比例，压缩图,强制压缩
        _cmd = u"magick convert -resize %sx%s! %s %s" % (_out_w,_out_h,img2_src,img2_src)
        subprocess.check_output(_cmd, shell=True)

        #gif合成
        _cmd = u" magick  -loop 0 %s %s  %s  " % (img1_src,  img2_src, save_url)
        subprocess.call(_cmd, shell=True)

        _cmd = u" magick  convert -colors 100  %s  %s" % (save_url,save_url)
        subprocess.call(_cmd, shell=True)

    #将图片设置为180比例的方块，若处理失败，直接删除该图片，跳错
    def Join_AddBackGround(self,img1_src,re_size=180):
        try:
            _re_size = re_size #显示尺寸，180x180
            img_src = img1_src
            img = self.Identity(img_src)  #获取图片1宽高
            img_w = float(img['width'])
            img_h = float(img['height'])
            if img_w >= img_h:
                border_x = 0
                border_y = int(( re_size - img_h ) / 2)
            else:
                border_x = int(( re_size - img_w ) / 2)
                border_y = 0
            #为图片加黑边
            _cmd = u'magick convert -border  %sx%s -bordercolor "#000000"  %s %s' % (border_x,border_y,img_src,img_src)
            # print _cmd
            subprocess.check_output(_cmd, shell=True)
        except Exception,e:
            print os.remove(img1_src)  #若处理失败 , 删除该图片，跳错
            raise e

    def Join_HasReize(self,img_src1,type1,img_src2,type2,save_path="",re_size=180):
        try:
            _out_range = 180
            _re_size = re_size #显示尺寸，180x180
            img1_src = img_src1
            _type1 = type1
            img2_src = img_src2
            _type2 = type2
            save_url = save_path

            #延时计算
            _delay1 = 150
            _delay2 = 150
            if _type1 == 'gif' or _type1 == "GIF" or _type1 == 'Gif':
                _delay1 = 0
            if _type2 == 'gif' or _type2 == "GIF" or _type2 == 'Gif':
                _delay2 = 0

            print "delay:",_delay1,_delay2
            # #gif合成
            if _delay1 == 0 and _delay2 == 0: #两张GIF
                _cmd = u" magick convert  %s   %s  -loop 0 %s  " % (img1_src,img2_src, save_url)  # 纯粹gif，不用延时
            if _delay1 != 0 and _delay2 == 0:  #第一张图片，第二张GIF
                print "wait"
                _cmd = u" magick convert  -delay %s  %s   %s  -loop 0 %s  " % (_delay1,img1_src,img2_src, save_url) #有jpg静态图片，需设置延时
            if _delay1 == 0 and _delay2 != 0:  #第一张GIF，第二张图片
                print "type 3"
                _cmd = u" magick convert %s  -delay %s %s  -loop 0 %s  " % (img1_src, _delay2 , img2_src, save_url) #有jpg静态图片，需设置延时
            if _delay1 != 0 and _delay2 != 0: #两张图片
                _cmd = u" magick convert  -delay %s  %s  -delay %s %s  -loop 0 %s  " % (_delay1,img1_src, _delay2 , img2_src, save_url) #有jpg静态图片，需设置延时

            subprocess.call(_cmd, shell=True)

            print datetime.datetime.now()
        except Exception,e:
            print os.remove(save_path)  #若处理失败 , 删除该图片，跳错
            raise e
        # img1 = self.Identity(img1_src)  #获取图片1宽高
        # img1_w = float(img1['width'])
        # img1_h = float(img1['height'])


        # def AddBackGround(img_src):
        #     img = self.Identity(img_src)  #获取图片1宽高
        #     img_w = float(img['width'])
        #     img_h = float(img['height'])
        #     if img_w >= img_h:
        #         border_x = 0
        #         border_y = int(( re_size - img_h ) / 2)
        #     else:
        #         border_x = int(( re_size - img_w ) / 2)
        #         border_y = 0
        #     #为图片加黑边
        #     _cmd = u'magick convert -border  %sx%s -bordercolor "#000000"  %s %s' % (border_x,border_y,img_src,img_src)
        #     # print _cmd
        #     subprocess.check_output(_cmd, shell=True)
        # print datetime.datetime.now()
        # AddBackGround(img1_src)
        # print datetime.datetime.now()
        # AddBackGround(img2_src)
        # print datetime.datetime.now()



        #
        # img2 = self.Identity(img2_src)  #获取图片2宽高
        # img2_w = float(img1['width'])
        # img2_h = float(img1['height'])



        # #按_out_range ，按固定比例压缩图片
        # _cmd = u"magick convert -resize %sx%s %s %s" % (_out_range,_out_range,img1_src,img1_src)
        # subprocess.check_output(_cmd, shell=True)
        #
        # #解析第一张图片压缩后数据,以此为模板
        # img1 = self.Identity(img1_src)
        # _out_w = float(img1['width'])
        # _out_h = float(img1['height'])
        # _out_r = _out_h/_out_w
        #
        # #按照图1的比例，压缩图2
        # _cmd = u"magick convert -resize %sx%s %s %s" % (_out_w,_out_h,img2_src,img2_src)
        # subprocess.check_output(_cmd, shell=True)
        #
        # #解析图二压缩后数据，
        # img2 = self.Identity(img2_src)
        # img2_w = float(img2['width'])
        # img2_h = float(img2['height'])
        #
        # #第2张图片偏移量
        # offsetY = int(( _out_h - img2_h ) /2)
        # offsetX = int(( _out_w - img2_w ) /2)
        # print _out_h,_out_w
        # print img2_h,img2_w
        #
        # #图片2加黑边
        # _cmd = u'magick convert -border  %sx%s -bordercolor "#000000"  %s %s' % (offsetX,offsetY,img2_src,img2_src)
        # subprocess.check_output(_cmd, shell=True)
        #
        #
        # #按照图1的比例，压缩图,强制压缩
        # _cmd = u"magick convert -resize %sx%s! %s %s" % (_out_w,_out_h,img2_src,img2_src)
        # subprocess.check_output(_cmd, shell=True)
        #
        # #gif合成
        # _cmd = u" magick  -loop 0 %s %s  %s  " % (img1_src,  img2_src, save_url)
        # subprocess.call(_cmd, shell=True)
        #
        # _cmd = u" magick  convert -colors 100  %s  %s" % (save_url,save_url)
        # subprocess.call(_cmd, shell=True)

    # 识别img的基础数据
    # 1\地址，2\格式，3\size，4\偏移量，5\8-bit，6\sRGB，7\256c,8\占用内存，9\0.000u， 10\时间
    #['C:\\Users\\Administrator\\Desktop\\vedio\\img2gif\\pre1.gif[0]', 'GIF', '96x128', '96x128+0+0', '8-bit', 'sRGB', '256c', '214KB', '0.000u', '0:00.003']
    def Identity(self,img_url):
        _cmd = u"magick identify %s" %(img_url)
        out_str = subprocess.check_output(_cmd, shell=True)
        arr = out_str.split('\r\n')
        frame = arr[0].split(' ')
        _space =  float(frame[7][:-2])
        if frame[7][-2:] == 'MB':
            _space = _space*1024

        #计算Geometry是否变化，
        _temp = frame[3]
        # print _temp
        _is_same_geometry = True
        for i in range(0,len(arr)-1):
            _temp_frame = arr[i].split(' ')
            # print _temp_frame
            if _temp == _temp_frame[3]:
                _is_same_geometry = False

        return {
            "frame_num":len(arr),
            "width": float(frame[2].split('x')[0]),
            "height":float(frame[2].split('x')[1]),
            "type":frame[1],
            "color_code":frame[5],
            "space":int(_space),
            "color":frame[6][:-1],
            "ratio":float(frame[2].split('x')[1])/float(frame[2].split('x')[0]), #高/宽比，
            "is_same_geometry":_is_same_geometry
        }

    #图片压缩，对外使用
    # gif :
    # 1MB以内、
    # 192*240、192*192、 128*128
    # color 64c 、 128c
    # png/jpg : 1280*720 大小不限制
    def Resize(self,in_src):

        print in_src
        img = self.Identity(in_src)
        print 2

        if(img['space'] < 1000):
            #复制图片
            _cmd = u"magick %s %s" %(in_src,self.save_url)
            out_str = subprocess.check_output(_cmd, shell=True)
            return

        if img['is_same_geometry'] is True:
            if(img['space'] > 1000 and img['space'] < 1500):
                # 180x240 裁剪
                _cmd = u"magick convert -resize 170x170 %s %s" % (in_src,self.save_url)
                subprocess.check_output(_cmd, shell=True)
                return

            if(img['space'] >= 1500 and img['space'] < 2000):
                # 128x128 裁剪
                _cmd = u"magick convert -resize 128x128 %s %s" % (in_src,self.save_url)
                subprocess.check_output(_cmd, shell=True)
                return
            if(img['space'] > 2000):
                # 96x96 裁剪
                _cmd = u"magick convert -resize 96x96 %s %s" % (in_src,self.save_url)
                subprocess.check_output(_cmd, shell=True)
                return
            # 颜色转换,对save图直接操作

        else:
            if(img['space'] > 1000 and img['space'] < 1500):
                _cmd = u"magick convert  %s -coalesce -thumbnail 170x170 -layers optimize %s" % (in_src,self.save_url)
                subprocess.check_output(_cmd, shell=True)
                return
            if(img['space'] >= 1500 and img['space'] < 2000):
                # 128x128 裁剪
                _cmd = u"magick convert  %s -coalesce -thumbnail 128x128 -layers optimize %s" % (in_src,self.save_url)
                subprocess.check_output(_cmd, shell=True)
                return
            if(img['space'] > 2200):
                # 96x96 裁剪
                _cmd = u"magick convert  %s -coalesce -thumbnail 96x96 -layers optimize %s" % (in_src,self.save_url)
                subprocess.check_output(_cmd, shell=True)
                return
            # 颜色转换,对save图直接操作

        _cmd = u"magick convert -colors 100 %s %s" % (img['color'],self.save_url,self.save_url)
        subprocess.check_output(_cmd, shell=True)

    #把图片copy到save_url
    def Copy(self,in_src):
        _cmd = u"magick %s %s" %(in_src,self.save_url)
        out_str = subprocess.check_output(_cmd, shell=True)
    def Video2Gif(self,url,save_path,startTime ,endTime ,resize ):

        _startTime = float(startTime)
        _endTime = float(endTime)
        _speed = 1.5
        _resize = float(resize) #把320*40的视频转192*144
        _fps = 10
        # print VideoFileClip(url)
        clip = (VideoFileClip(url)
                .subclip((0,_startTime),(0,_endTime))
                .speedx(_speed)
                .resize(_resize)
                # .fx(vfx.freeze_region, outside_region=(170, 230, 380, 320))
                )
        clip.write_gif(save_path, fps=_fps)

import  datetime
import sys
print sys.argv
if __name__ ==  "__main__":
    # print "Program name", sys.argv[0], sys.argv[1], sys.argv[2], sys.argv[3]
    url = sys.argv[1]
    save_url = sys.argv[2]
    start_time = sys.argv[3]
    end_time = sys.argv[4]
    resize = sys.argv[5]
    # print url,save_url,start_time,end_time
    m = Magick()
    m.Video2Gif(url,save_url,start_time,end_time,resize)


    # a = datetime.datetime.now()
    #
    # img1_src = r"C:\Users\Administrator\Desktop\vedio\img2gif\m1.gif"
    # img2_src = r"C:\Users\Administrator\Desktop\vedio\img2gif\h1.gif"
    # bg_src = r"C:\Users\Administrator\Desktop\vedio\img2gif\black.jpg"
    #
    #
    # img = r"C:\Users\Administrator\Desktop\vedio\gif\c.gif"
    # save_url = r"C:\Users\Administrator\Desktop\vedio\gif\c3.gif"
    # imgList = [img1_src,bg_src,img2_src]
    # # imgList = [img2_src,bg_src,img1_src]
    # # m.Image2Gif(imgList)
    # m.AddWatermark(img1_src)
    #
    #
    # print 'begin:',datetime.datetime.now()
    # datetime.
