#--coding:utf-8--
import os
from PIL import Image, ImageDraw,ImageFont

class ImageMix():
    def image_word(self,jpg_opt,word_opt):
        bg_url = jpg_opt["url"]
        bg_save_url = jpg_opt["save_url"]
        _im = Image.open(bg_url)
        _draw =ImageDraw.Draw(_im)
        for i in range(0,len(word_opt)):
            w = word_opt[i]
            word = w["word"]
            w_x = w["x"]
            w_y = w["y"]
            font = ImageFont.truetype('simsun.ttc',w["size"])
            _draw.text( (w_x,w_y),word,font=font,fill=(0,0,0) )
        _im.save(bg_save_url)
if __name__ == "__main__":
        jpg_opt = {
            "url": r"E:\Carcer World\code\Python\git\image_str\image_server\grid\static\mix\img_word.jpg",
            "save_url":r"E:\Carcer World\code\Python\git\image_str\image_server\grid\static\mix\img_word_save1.jpg",
        }
        word_opt = [
            {
                "word":u"我踩你",
                "size":18,
                "x":100,
                "y":50,
            },
            {
                "word":u"再踩你一次",
                "size":28,
                "x":300,
                "y":250,
            },
        ]
        m = ImageMix()
        m.image_word(jpg_opt,word_opt)