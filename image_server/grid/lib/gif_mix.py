#--coding:utf-8--
import os
from PIL import Image
import images2gif

class GifMix():
    #type 合成GIF分类
    #0：图片缩放到最大宽度*最大高度（长方形）、并粘贴到最大宽度*最大高度（长方形）的白色背景图片中、居中后合成
    #1：图片缩放到最大长度（正方形）、并粘贴到最大长度（正方形）的白色背景图片中、居中后合成
    #2：图片不缩放、并粘贴到最大宽度*最大高度（长方形）的白色背景图片中、居中后合成
    #3：图片不缩放、并粘贴到最大长度（正方形）的白色背景图片中、居中后合成
    #4：原图直接合成(按宽度排序、不缩放也不粘贴到新的白色背景图片中)
    #5：原图直接合成(按高度排序、不缩放也不粘贴到新的白色背景图片中)
    def GetGifAnimationFromImages(self,targetGifFilePath, srcImageFilePaths, type = 0):
        #用来合成的图片
        images = []

        #取得所有图片中最大长度（宽度、高度）
        maxWidthAndHeight = 1
        #最大宽度和高度
        maxWidth = 1
        maxHeight = 1
        #取得图片按宽度从大到小排序的路径顺序
        widthAndFilePaths = []
        #取得图片按高度从大到小排序的路径顺序
        heightAndFilePaths = []

        for imageFilePath in srcImageFilePaths:
            fp = open(imageFilePath, "rb")
            width,height = Image.open(fp).size
            widthAndFilePaths.append((width, imageFilePath))
            heightAndFilePaths.append((height, imageFilePath))
            maxWidth = max(maxWidth, width)
            maxHeight = max(maxHeight, height)
            fp.close()

        maxWidthAndHeight = max(maxWidthAndHeight, maxWidth, maxHeight)

        #降序排列
        widthAndFilePaths.sort(key=lambda item: item[0], reverse=True)
        heightAndFilePaths.sort(key=lambda item: item[0], reverse=True)

        if type == 4 or type == 5:
            #原图直接合成(按宽度排序)
            if type == 4:
                for widthAndFilePath in widthAndFilePaths:
                    img = Image.open(widthAndFilePath[1])
                    images.append(img)
            #原图直接合成(按高度排序)
            if type == 5:
                for heightAndFilePath in heightAndFilePaths:
                    img = Image.open(heightAndFilePath[1])
                    images.append(img)
        else:
            for imageFilePath in srcImageFilePaths:
                fp = open(imageFilePath, "rb")
                img = Image.open(fp)
                width,height = img.size
                #生成空的白色背景图片
                if type == 0 or type == 2:
                    #长方形
                    imgResizeAndCenter = Image.new("RGB", [maxWidth,maxHeight], (255,255,255))
                elif type == 1 or type == 3:
                    #正方形
                    imgResizeAndCenter = Image.new("RGB", [maxWidthAndHeight,maxWidthAndHeight], (255,255,255))

                if type == 0:
                    #宽度/最大宽度>=高度/最大高度，使用小的缩放比例
                    if maxWidth / width >= maxHeight / height:
                        resizeImg = img.resize((width * maxHeight / height, maxHeight),Image.ANTIALIAS)
                        imgResizeAndCenter.paste(resizeImg, ((maxWidth - width * maxHeight / height)/ 2,0))
                    else:
                        resizeImg = img.resize((maxWidth, height * maxWidth / width),Image.ANTIALIAS)
                        imgResizeAndCenter.paste(resizeImg, (0,(maxHeight - height * maxWidth / width)/ 2))
                if type == 1:
                    #宽度>=高度，按宽度缩放到最大长度
                    if width >= height:
                        resizeImg = img.resize((maxWidthAndHeight, height * maxWidthAndHeight / width),Image.ANTIALIAS)
                        imgResizeAndCenter.paste(resizeImg, (0,(maxWidthAndHeight - height * maxWidthAndHeight / width)/ 2))
                    else:
                        resizeImg = img.resize((width * maxWidthAndHeight / height, maxWidthAndHeight),Image.ANTIALIAS)
                        imgResizeAndCenter.paste(resizeImg, ((maxWidthAndHeight - width * maxWidthAndHeight / height)/ 2, 0))
                elif type == 2:
                    imgResizeAndCenter.paste(img, ((maxWidth - width) / 2,(maxHeight - height) / 2))
                elif type == 3:
                    imgResizeAndCenter.paste(img, ((maxWidthAndHeight - width) / 2,(maxWidthAndHeight - height) / 2))

        #        #保存缩放居中后的图片
        #        imgResizeAndCenter.convert("RGB").save(os.path.dirname(imageFilePath) + os.sep + "ResizeAndCenter" + os.path.basename(imageFilePath), 'jpeg')
                images.append(imgResizeAndCenter)
                fp.close()

        # images2gif.writeGif(targetGifFilePath, images, duration=0.05, nq=0.1)
        images2gif.writeGif(targetGifFilePath, images, duration=0.05,nq=0.1)

    #取得目录下面的文件列表
    def GetDirImageList(self,dir_proc, recusive = True):
        resultList = []
        for file in os.listdir(dir_proc):
            if os.path.isdir(os.path.join(dir_proc, file)):
                if (recusive):
                    resultList.append(self.GetDirImageList(os.path.join(dir_proc, file), recusive))
                continue

            resultList.append(os.path.join(dir_proc, file))

        return resultList


    #这个类不用了
    def MixImageList(self,bg_url,sprite_url_list,frame_url_list,option):
        try:
            offsetX = option["offsetX"]
            offsetY = option["offsetY"]
            out_width = option["out_width"]
            out_height = option["out_height"]

            #提取精灵图，重新绘制每一帧
            for i in range(0,len(sprite_url_list)):
                bg_im = Image.open(bg_url)
                sprite_im = Image.open(sprite_url_list[i])
                bg_im.paste(sprite_im, (offsetX,offsetY), sprite_im.convert('RGBA'))

                bg_im = bg_im.resize((out_width,out_height), Image.NEAREST)

                bg_im.save(frame_url_list[i], 'png')
            return True
        except Exception ,e:
            raise e

    def MixBgGifDraw(self,layer,bg,gif,draw,out):

        layer_list = layer

        bg_url = bg["bg_url"]
        bg_width = bg["bg_width"]
        bg_height = bg["bg_height"]

        gif_sprite_url_list =  gif["gif_sprite_url_list"]
        gif_offsetX =  gif["gif_offsetX"]
        gif_offsetY =  gif["gif_offsetY"]
        gif_width =  gif["gif_width"]
        gif_height =  gif["gif_height"]
        gif_show_width =  gif["gif_show_width"]
        gif_show_height =  gif["gif_show_height"]

        draw_url = draw["draw_url"]
        draw_offsetX = draw["draw_offsetX"]
        draw_offsetY = draw["draw_offsetY"]
        draw_width = draw["draw_width"]
        draw_height = draw["draw_height"]
        draw_show_width =  draw["draw_show_width"]
        draw_show_height =  draw["draw_show_height"]

        out_frame_url_list = out["out_frame_url_list"]
        out_url = out["out_url"]
        out_width = out["out_width"]
        out_height = out["out_height"]

        #除开背景，其他图像读入缓存
        gif_sprite_im_list = []
        for s_url in gif_sprite_url_list:
            gif_sprite_im_list.append( Image.open(s_url).resize((gif_show_width,gif_show_height), Image.NEAREST) ) #读取图片,缩放

        draw_im = Image.open(draw_url).resize((draw_show_width,draw_show_height), Image.NEAREST)

        #TODO 输出w,h预处理，貌似也不用做

        #复制拼接图像
        for i in range(0,len(gif_sprite_im_list)):
            bg_im = Image.open(bg_url)
            if layer_list[1] == 'draw':#先画draw,再画GIF
                bg_im.paste(draw_im, (draw_offsetX,draw_offsetY), draw_im.convert('RGBA'))
                bg_im.paste(gif_sprite_im_list[i], (gif_offsetX,gif_offsetY), gif_sprite_im_list[i].convert('RGBA'))
            else :
                bg_im.paste(gif_sprite_im_list[i], (gif_offsetX,gif_offsetY), gif_sprite_im_list[i].convert('RGBA'))
                bg_im.paste(draw_im, (draw_offsetX,draw_offsetY), draw_im.convert('RGBA'))
            bg_im = bg_im.resize((out_width,out_height), Image.NEAREST)
            bg_im.save(out_frame_url_list[i], 'png')

        return True


        # bg_im = bg_im.resize((out_width,out_height), Image.NEAREST)

        # bg + mark 两张拼接
        # def PasteBgImage(bg_url,paste_url,out_url,offsetX,offsetY,out_width,out_height, out_style = "png"):
        #     try:
        #         bg_im = Image.open(bg_url)
        #         paste_im = Image.open(paste_url)
        #         bg_im.paste(paste_im, (offsetX,offsetY), paste_im.convert('RGBA'))
        #         bg_im = bg_im.resize((out_width,out_height), Image.NEAREST)
        #         bg_im.save(out_url, out_style)
        #     except Exception ,e:
        #         raise e



if __name__ == "__main__":  
    # GetGifAnimationFromImages(r"D:\\hecheng_littile.gif", [r"http://7xsark.com1.z0.glb.clouddn.com/img/20160823110421.png", r"http://7xsark.com1.z0.glb.clouddn.com/img/20160823110421.png", r"http://7xsark.com1.z0.glb.clouddn.com/img/20160823110421.png"])
    # GetGifAnimationFromImages(r"D:\\hecheng1.gif", [r"D:\\a.jpg", r"D:\\b.jpg", r"D:\\b.jpg", r"D:\\c.jpg"], 1)
    # GetGifAnimationFromImages(r"D:\\hecheng2.gif", [r"D:\\a.jpg", r"D:\\b.jpg", r"D:\\c.jpg"], 2)
    # GetGifAnimationFromImages(r"D:\\hecheng3.gif", [r"D:\\a.jpg", r"D:\\b.jpg", r"D:\\c.jpg"], 3)
    # GetGifAnimationFromImages(r"D:\\hecheng4.gif", [r"D:\\a.jpg", r"D:\\b.jpg", r"D:\\c.jpg"], 4)
    # GetGifAnimationFromImages(r"D:\\hecheng5.gif", [r"D:\\a.jpg", r"D:\\b.jpg", r"D:\\c.jpg"], 5)

    # GetGifAnimationFromImages(r"D:\\hecheng_png1.gif", GetDirImageList(r"D:\\GifMarker1"), type = 4)
    # GetGifAnimationFromImages(r"D:\\hecheng_png1.gif", GetDirImageList(r"D:\\GifMarker1"), type = 4)

    path = r'C:\Users\Administrator\Desktop\gif\\'
    bg_url = path + r'bg.jpg'
    sprite_url_list = [path + r'a.png',path + r'b.png',path + r'c.png']
    frame_url_list = [path + r'save_fame_11.jpg',path + r'save_fame_12.jpg',path + r'save_fame_13.jpg',]
    save_gif_url =  path + r'user.gif'

    option = {
         "offsetX":100,
         "offsetY":100,
         "out_width":256,
         "out_height":192
    }

    layer = ["bg","draw","gif"]


    bg = {
        "bg_url":path + r'bg.jpg',
        "bg_width":240,
        "bg_height":240,
    }
    gif = {
        "gif_sprite_url_list":[path + r'a.png',path + r'b.png',path + r'c.png'],
        "gif_offsetX":100,
        "gif_offsetY":100,
        "gif_width":240,
        "gif_height":240,
        "gif_show_width":120,
        "gif_show_height":120,
    }
    draw = {
        "draw_url":path + r'a.png',
        "draw_offsetX":200,
        "draw_offsetY":200,
        "draw_width":240,
        "draw_height":240,
        "draw_show_width":120,
        "draw_show_height":120,
    }
    out= {
        "out_frame_url_list":[path + r'save_fame_11.jpg',path + r'save_fame_12.jpg',path + r'save_fame_13.jpg',],
        "out_url": path + r'user.gif',
        "out_width":256,
        "out_height":192,
    }


    # g = GifMix()
    # g.GetGifAnimationFromImages(r"C:\Users\Administrator\Desktop\vedio\d_53.gif", g.GetDirImageList(r"C:\Users\Administrator\Desktop\vedio\picture"), type = 4)
    #
    # #bg + gif + draw
    # if g.MixBgGifDraw(layer,bg,gif,draw,out):
    #     g.GetGifAnimationFromImages(out["out_url"], out["out_frame_url_list"])

    #bg + gif
    # if g.MixImageList(bg_url,sprite_url_list,frame_url_list,option):
    #      g.GetGifAnimationFromImages(save_gif_url, frame_url_list)


    url = r"H:\Code\Python\Git\image_str\image_server\grid\static\mix"
    im = Image.open("filename")


#该片段来自于http://outofmemory.cn