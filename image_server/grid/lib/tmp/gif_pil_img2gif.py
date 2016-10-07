#--coding:utf-8--
import imageio


images = []
# path = r'H:\Code\Python\Git\image_str\image_server\grid\lib\tmp\tmp\\'
path = r'H:\Code\Python\Git\ffmpeg\test\picture3\image'
filenames = []
for i in range(1,28):
    filenames.append(path+ str(i) + ".png")
for filename in filenames:
    images.append(imageio.imread(filename))
imageio.mimsave('movie1.gif', images)


from PIL import Image, ImageSequence
#
# gif_path = r'H:\Code\Python\Git\image_str\image_server\grid\static\mix\user1.gif'
# # im = Image.open("D:\\Code\\Python\\test\\img\\test01.gif")
# im = Image.open(gif_path)
#
# index = 1
# for frame in ImageSequence.Iterator(im):
#     print "image: index %d, mode %s, size %s" % (index, frame.mode, frame.size)
#     frame.convert('P').save("frame%d.png" % index)
#     index = index + 1
#
# iter = ImageSequence.Iterator(im)
# print "image 10: mode %s, size %s" % (iter[10].mode, iter[10].size)
# iter[10].show()


# def iter_frames(im):
#     try:
#         i= 0
#         while 1:
#             im.seek(i)
#             im = im.copy()
#             im.palette.dirty = 1
#             im.palette.rawmode = "RGB"
#             if i == 0:
#                 palette = im.getpalette()
#             else:
#                 im.putpalette(palette)
#             # print palette
#             yield im
#
#             # imframe = im.copy()
#             # imframe.palette.dirty = 1
#             # imframe.palette.rawmode = "RGB"
#             # if i == 0:
#             #     palette = imframe.getpalette()
#             # else:
#             #     imframe.putpalette(palette)
#             # # print palette
#             # yield imframe
#             i += 1
#     except EOFError:
#         pass
#
#
# gif_path = r'H:\Code\Python\Git\image_str\image_server\grid\static\mix\user2.gif'
# im = Image.open(gif_path)
# for i, frame in enumerate(iter_frames(im)):
#     frame.save('test%d.png' % i,**frame.info)


# gif_path = r'H:\Code\Python\Git\image_str\image_server\grid\static\mix\user2.gif'
# # im = Image.open("D:\\Code\\Python\\test\\img\\test01.gif")
# from PIL import Image
#
# im = Image.open(gif_path)
# # transparency = im.info['transparency']
# transparency = None
# p = im.palette.getdata()[1]
# im.save('test1.png',"PNG", transparency=transparency)
# im.seek(im.tell()+1)
#
# im.putpalette(p)
# im.palette.dirty = 1
# im.palette.rawmode = "RGB"
# im.palette.mode = "RGB"
# # transparency = im.info['transparency']
# transparency = None
# im.save('test2.png',"PNG", transparency=transparency)

# from PIL import Image
#
# gif_path = r'H:\Code\Python\Git\image_str\image_server\grid\static\mix\user2.gif'
# img = Image.open(gif_path)
#
# counter = 0
# collection = []
# current = img.convert('RGBA')
# while True:
#     try:
#         current.save('original%d.png' % counter)
#         img.seek(img.tell()+1)
#         current = Image.alpha_composite(current, img.convert('RGBA'))
#         counter += 1
#     except EOFError:
#         break