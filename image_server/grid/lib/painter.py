#--coding:utf-8--
from PIL import Image,ImageDraw,ImageFont
import sys
import  os
import  time

class CharImage():
    def __init__(self):
        self.ascii = list(u"X/-.  ") #
        self.gray = 255
        self.grid = 4   #格子数

        self.size = 10 # 字符绘制宽度
        self.c_w = 128 # 字符画 固定 宽
        self.c_h = 128 # 自适应 高

        self.im = None #
        self.c_im = None #


    def setAsciiStr(self,ascii):
        self.ascii = str(ascii)
    def setGridNum(self,grid):
        self.grid = int(grid)
    def setPixelSize(self,char_size):
        self.size = int(char_size)

    #pre 必选项 准备原图
    def PreImage(self,url):
        _im = Image.open(url)
        _im_w = _im.size[0]
        _im_h = _im.size[1]
        self.c_h = int(( float(_im_h) / float(_im_w) ) * float(self.c_w)) #
        self.im = _im.resize((self.c_w,self.c_h), Image.NEAREST) #
    #pre 必选项 准备字符图
    def PreCharImage(self):
        self.c_im = Image.new("RGBA",(self.c_w*self.size,self.c_h*self.size),(255,255,255)) #

    #r g b 对应 字符
    def _Get_Char(self,r,g,b,alpha = 256):
        if alpha == 0:
            return ' '
        gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)

        unit = (256.0 + 1 - self.gray)/ len(self.ascii) #根据自己灰度阶 内部比较
        return self.ascii[int( (gray - self.gray)/unit)]

        # unit = (256.0 + 1)/ len(self.ascii) #全灰度阶比较
        # return self.ascii[int(gray/unit)]


    def _Max_Gray(self,r,g,b,alpha = 256):
        if alpha == 0:
            return ' '
        gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
        if gray < self.gray :
            self.gray = gray

    #画字符
    def DrawCharImage(self):
        _draw =ImageDraw.Draw(self.c_im)

        #计算灰度最小（最暗）的值
        for i in range(self.c_h):
            for j in range(self.c_w):
                self._Max_Gray(*self.im.getpixel((j,i)))

        for i in range(self.c_h):
            for j in range(self.c_w):
                _char = self._Get_Char(*self.im.getpixel((j,i)))
                _draw.text((j*self.size,i*self.size),_char,fill=(0,0,0))

        print 'OK'
    #计算方格line 列表
    def _Get_Line(self,width = 1080,height = 1920,numX = 4):
        offX = width % numX / 2
        length = (width - offX * 2) / numX
        numY = height / length  #
        offY = height % length / 2
        _lines = []
        #
        for i in range(numY+1):
            _lines.append( (offX,offY + length*i,offX + length * numX , offY + length*i) )
        #
        for i in range(numX+1):
            _lines.append( (offX + length * i,offY,offX + length * i , offY + length * numY) )
        return _lines

    #画方格
    def DrawGrid(self):
        _draw =ImageDraw.Draw(self.c_im)
        _color = (130, 130, 130)
        #
        _lines = self._Get_Line(self.c_w*self.size,self.c_h*self.size,self.grid)
        #
        for i in range(len(_lines)):
            _draw.line([(_lines[i][0],_lines[i][1]),(_lines[i][2],_lines[i][3])],fill=_color,width=1)

    #保存
    def Save(self,path):
        self.c_im.save(path)

#
class Painter():
    #字符画+方格
    @staticmethod
    def CharGrid(url,save_path):
        _cim = CharImage()
        _cim.PreImage(url)
        _cim.PreCharImage()
        _cim.DrawCharImage()
        _cim.DrawGrid()
        _cim.Save(save_path)
        return True
    #字符画
    @staticmethod
    def Char(url,save_path):
        _cim = CharImage()
        _cim.PreImage(url)
        _cim.PreCharImage()
        _cim.DrawCharImage()
        _cim.Save(save_path)
        return True
        # print  _cim._Get_Line()
