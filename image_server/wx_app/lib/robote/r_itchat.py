# -*- coding: utf-8 -*-
import itchat, time
from itchat.content import *
from filter import Filter
import glob
import random

#群消息
# @itchat.msg_register(TEXT, isFriendChat=True, isGroupChat=True, isMpChat=True)
# def general_reply(msg):
#     return 'I received a %s' % msg['Type']

#私聊
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    print msg
    # with open("t.txt", "wb") as code:
    #     code.write(str(msg))
    if  msg['Type'] == 'Sharing':
        imgFilter = Filter()
        img_list = imgFilter.getContents(msg['Url'])
        i=0
        for img in img_list:
            print img_list,img,i
            i = i+1
            itchat.send('@img@%s' % str(i)+".gif" ,msg['FromUserName'])
    # print msg['MsgType'],msg['AppMsgType'],msg['FromUserName'],msg['ToUserName'],msg['Url'],msg['FileName'],msg['Content']
    # itchat.send('%s: %s' % (msg['Type'], msg['Text']), msg['FromUserName'])
    # itchat.send('%s: %s' % (msg['Type'], msg['Url']), msg['FromUserName'])
    # itchat.send('%s: %s' % (msg['Type'], msg['Content']), msg['FromUserName'])
    # itchat.send('@img@%s' % '170210-105741.gif',msg['FromUserName'])
    # itchat.send('@img@%s' % '170210-105741.gif',msg['FromUserName'])
    # itchat.send('%s: %s' % (msg['Type'], msg['Text']), msg['FromUserName'])

@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    print msg['MsgType']
    print msg['Content']
    # msg['Text'](msg['FileName'])
    # url = {'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil')
    # msg = msg['FileName']
    # # print msg
    # print  url,msg


    _gif_all =  glob.glob(r"E:\CarcerWorld\code\Python\git\image_str\image_server\wx_app\lib\robote/*.gif")

    print _gif_all[0]
    # itchat.send('@%s@%s' % (url,_gif_all[0]), msg['FromUserName'])

    msg['Text'](msg['FileName'])
    # return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])
    _ran_index = int(random.random()*(len(_gif_all)-1))
    return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), _gif_all[_ran_index])

    # print msg['MsgType']
    # print msg['Content']
    # print msg['MsgType'],msg['AppMsgType'],msg['FromUserName'],msg['ToUserName'],msg['Url'],msg['FileName'],msg['Content']
    # itchat.send('@%s@%s' % (url,msg), msg['FromUserName'])
    # itchat.send('%s' % ( msg['Content'] ), msg['FromUserName'])
    # return '@%s@%s' % (url,msg)

@itchat.msg_register(FRIENDS)
def add_friend(msg):
    # print msg
    itchat.add_friend(**msg['Text']) # 该操作会自动将新好友的消息录入，不需要重载通讯录
    # itchat.send_msg('Nice to meet you!', msg['RecommendInfo']['UserName'])
    itchat.send_msg(u'公众号信息分享给我，所有图片自动转表情', msg['RecommendInfo']['UserName'])
    itchat.send_msg(u'存储空间不够了？搜索“表情袋”，斗图再多也能存!', msg['RecommendInfo']['UserName'])

@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    # print msg
    if msg['isAt']:
        itchat.send(u'@%s\u2005I received: %s' % (msg['ActualNickName'], msg['Content']), msg['FromUserName'])

@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO], isGroupChat=True)
def download_files_group(msg):
    pass
    print msg["Type"], msg["MsgType"] , msg['Url']
    msg['Text'](msg['FileName'])
    # if msg['isAt']:
    #     msg['Text'](msg['FileName'])
    #     return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])

itchat.auto_login(hotReload=True)
itchat.run()


