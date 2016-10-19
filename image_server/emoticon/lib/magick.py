#--coding:utf-8--
from moviepy.editor import *
import subprocess
import logging
import os
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
class Magick():
    save_url = ""
    def __init__(self,save_url):
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
    def Video2Gif(self,startTime = 0,endTime = 6,url = r"C:\Users\Administrator\Desktop\vedio\draw.mp"):

        _startTime = float(startTime)
        _endTime = float(endTime)
        _speed = 3
        _resize = float(192.00/320.00) #把320*40的视频转192*144
        _fps = 10
        try:
        # print VideoFileClip(url)
            clip = (VideoFileClip(url)
                    .subclip((0,_startTime),(0,_endTime))
                    .speedx(_speed)
                    .resize(_resize)
                    # .fx(vfx.freeze_region, outside_region=(170, 230, 380, 320))
                    )
            clip.write_gif(self.save_url, fps=_fps)
            return True
        except Exception:
            # logger.error(Exception)
            return False


    # 两张图片拼Gif
    # 以第一张图片Wie模板
    # 固定128的大小
    def Join(self,imgList=[]):
        _out_range = 150
        img1_src = imgList[0]
        bg_src = imgList[1]
        img2_src = imgList[2]

        img1_pre_src = BASE_DIR + "/static/magick/temp/pre1.gif"
        img2_pre_src = BASE_DIR + "/static/magick/temp/pre2.gif"
        bg_pre_src = BASE_DIR + "/static/magick/temp/pre_black.jpg"

        #按128x128，按固定比例压缩图片
        _cmd = u"magick convert -resize %sx%s %s %s" % (_out_range,_out_range,img1_src,img1_pre_src)
        subprocess.check_output(_cmd, shell=True)

        #解析第一张图片压缩后数据,以此为模板
        img1 = self.Identity(img1_pre_src)
        _out_w = float(img1['width'])
        _out_h = float(img1['height'])
        _out_r = _out_h/_out_w

         #按照图1的范围，压缩黑色背景图
        _cmd = u"magick convert -resize %sx%s! %s %s" % (_out_w,_out_h,bg_src,bg_pre_src)
        subprocess.check_output(_cmd, shell=True)

        #按照图1的范围，压缩图2
        _cmd = u"magick convert -resize %sx%s %s %s" % (_out_w,_out_h,img2_src,img2_pre_src)
        subprocess.check_output(_cmd, shell=True)

        #解析图二压缩后数据，
        img2 = self.Identity(img2_pre_src)
        img2_w = float(img2['width'])
        img2_h = float(img2['height'])

        #第2张图片偏移量
        offsetY = int(( _out_h - img2_h ) /2)
        offsetX = int(( _out_w - img2_w ) /2)
        print _out_h,_out_w
        print img2_h,img2_w
        # print bord_h,bord_w
        # _cmd = u" magick  -delay 50 -loop 0 %s %s  %s  " % (img1_pre_src, bg_pre_src,  self.save_url)
        # subprocess.call(_cmd, shell=True)
        # _cmd = u" magick   -loop 0  %s ( %s -repage 0x0+%s+%s! )  %s  " % (self.save_url, img2_pre_src, offsetX, offsetY, self.save_url)
        # subprocess.call(_cmd, shell=True)
        _cmd = u" magick  -loop 0 %s %s ( %s -repage 0x0+%s+%s! )  %s  " % (img1_pre_src, bg_pre_src, img2_pre_src, offsetX, offsetY, self.save_url)
        subprocess.call(_cmd, shell=True)

        _cmd = u" magick  convert -colors 100  %s  %s" % (self.save_url,self.save_url)
        subprocess.call(_cmd, shell=True)

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
        return {
            "frame_num":len(arr),
            "width": float(frame[2].split('x')[0]),
            "height":float(frame[2].split('x')[1]),
            "type":frame[1],
            "color_code":frame[5],
            "space":int(_space),
            "color":frame[6][:-1],
            "ratio":float(frame[2].split('x')[1])/float(frame[2].split('x')[0]), #高/宽比，
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

        if(img['space'] > 1000 and img['space'] < 1500):
            # 180x240 裁剪
            _cmd = u"magick convert -resize 180x240 %s %s" % (in_src,self.save_url)
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
        _cmd = u"magick convert -colors %s %s %s" % (img['color'],self.save_url,self.save_url)
        subprocess.check_output(_cmd, shell=True)

    #把图片copy到save_url
    def Copy(self,in_src):
        _cmd = u"magick %s %s" %(in_src,self.save_url)
        out_str = subprocess.check_output(_cmd, shell=True)


import  datetime
if __name__ ==  "__main__":

    a = datetime.datetime.now()

    img1_src = r"C:\Users\Administrator\Desktop\vedio\img2gif\m1.gif"
    img2_src = r"C:\Users\Administrator\Desktop\vedio\img2gif\h1.gif"
    bg_src = r"C:\Users\Administrator\Desktop\vedio\img2gif\black.jpg"


    img = r"C:\Users\Administrator\Desktop\vedio\gif\c.gif"
    save_url = r"C:\Users\Administrator\Desktop\vedio\gif\c3.gif"
    imgList = [img1_src,bg_src,img2_src]
    # imgList = [img2_src,bg_src,img1_src]
    m = Magick(save_url)
    # m.Image2Gif(imgList)
    m.AddWatermark(img1_src)
    # m.Resize(img)


    print 'begin:',datetime.datetime.now()
    # datetime.
