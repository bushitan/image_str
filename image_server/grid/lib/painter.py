#--coding:utf-8--

from PIL import Image,ImageDraw,ImageFont
import sys
import  os
import  time
import  random
import colorsys

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

    def GetCirclePosition(self):
        print 'ok'
        _position_dict = {0:[],1:[],2:[],3:[],4:[],5:[]}#点分5级
        # _choice_num_dict = [5,20,15,5,5]
        _choice_num = [1,2,2,1,1,1] #6个指标
        for i in range(self.c_h):
            for j in range(self.c_w):
                _level = self._Get_PixelLevel(*self.im.getpixel((j,i)))
                # print _level
                _position_dict[_level].append( {'x':j,'y':i} )#加入坐标

        # print _position_dict
        #可能存在重复
        def RanChoice(pos_list,num):
            try:
                _num = num #随机选择的个数
                _index = 0 #索引位置
                _lenght = len(pos_list) #数组长度
                _list = [] #最新的结果

                #保证选取的数量不超过数组长度
                if _lenght < num:
                    _num = _lenght

                for i in range(0,_lenght):
                    if _index < _num: #所以总数量，执行摇色子
                        _ran_index = random.randint(0, _lenght - _index - 1)
                        print _ran_index
                        _list.append( pos_list[_ran_index] ) #记录选中坐标
                        print  pos_list[_ran_index]
                        _index = _index + 1
                    else:
                        break

                return _list
            except Exception ,e:
                print e

        # #随机选择 50个 (25对)点
        _new_position_dict =  {0:[],1:[],2:[],3:[],4:[],5:[]}
        for i in range(0,6):
            _new_position_dict[i] = RanChoice(_position_dict[i],_choice_num[i])

        # print _new_position_dict
        #绝对不重复
        def RandomChoice(pos_list,num):
            _num = num #随机选择的个数
            _index = 0 #索引位置
            _lenght = len(list) #数组长度
            _list = [] #最新的结果

            if _lenght < num:
                _num = _lenght

            for i in range(0,_lenght):
                if _index < _num: #所以总数量，执行摇色子
                    _ran_index = random.randint(0, _lenght - _index - 1)
                    _list.append( pos_list[_ran_index] ) #记录选中坐标
                    #位置互换
                    temp = pos_list[_lenght-1]
                    pos_list[_lenght-1] = pos_list[_ran_index]
                    pos_list[_ran_index] = temp
                    _index = _index + 1
                else:
                    break
            return _list

        return _new_position_dict


    def _Get_PixelLevel(self,r,g,b,alpha = 256):
        if alpha == 0:
            return ' '
        gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)

        unit = (256.0 + 1 - self.gray)/ len(self.ascii) #根据自己灰度阶 内部比较
        return int( (gray - self.gray)/unit)

    def GetMainColor(self):
        image = self.im.convert('RGBA')
        max_score = None
        dominant_color = None

        color_list = []
        for count, (r, g, b, a) in image.getcolors(image.size[0] * image.size[1]):
            # 跳过纯黑色
            if a == 0:
                continue

            saturation = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)[1]

            y = min(abs(r * 2104 + g * 4130 + b * 802 + 4096 + 131072) >> 13, 235)

            y = (y - 16.0) / (235 - 16)

            # 忽略高亮色
            if y > 0.9:
                continue

            # Calculate the score, preferring highly saturated colors.
            # Add 0.1 to the saturation so we don't completely ignore grayscale
            # colors by multiplying the count by zero, but still give them a low
            # weight.
            score = (saturation + 0.1) * count

            if score > max_score:
                max_score = score
                dominant_color = (r, g, b)
                color_list.append(dominant_color)

        return color_list


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

    #
    @staticmethod
    def Game_ActiveCircle(url,save_path):
        _cim = CharImage()
        _cim.PreImage(url)
        _cim.PreCharImage()
        _cim.DrawCharImage()
        # _cim.Save(save_path)

        _circle_dict = _cim.GetCirclePosition() #获取圈的位置
        _color_dict = _cim.GetMainColor() # 获取图片主要颜色
        # print 'color :' ,_color_dict
        return {'circle':_circle_dict,'color':_color_dict}


if __name__ == '__main__':
    _position = {
            1:[]
        }

    a = 1
    _position[a].append(11)
    print _position

    temp_dict =  {0:[],1:[],2:[],3:[],4:[],5:[]}
    for i in range(0,6):
            temp = [{'x':5,'y':10}]
            print temp
            temp_dict[i] = temp
    print temp_dict