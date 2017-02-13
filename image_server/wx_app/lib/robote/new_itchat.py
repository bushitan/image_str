# -*- coding: utf-8 -*-
import new_itchat as itchat , time
from new_itchat.content import *
import new_itchat.config as config
from filter import Filter
import glob
import random
import requests
import json
#群消息
# @itchat.msg_register(TEXT, isFriendChat=True, isGroupChat=True, isMpChat=True)
# def general_reply(msg):
#     return 'I received a %s' % msg['Type']

#私聊
AUTO_REPLY = {}


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    print msg
    # with open("t.txt", "wb") as code:
    #     code.write(str(msg))
    content = msg['Content']
    if msg['FromUserName'] == msg['ToUserName']:
        print content
        WORD_CLEAR = u"自助回复清除成功"
        WORD_ADD = u"自助回复增加成功"
        WORD_UPDATE = u"自助回复更新成功"
        if content == "QC": #清除
            AUTO_REPLY.clear()
            itchat.send('%s' % (WORD_CLEAR), msg['FromUserName'])
            return
        if content == "QU":
            _reply_dict = server.updateReply()
            print "re:",_reply_dict
            AUTO_REPLY.clear()
            for i in _reply_dict:
                AUTO_REPLY[i] = _reply_dict[i]
            print "auto:",AUTO_REPLY
            itchat.send('%s' % (WORD_UPDATE), msg['FromUserName'])
            return
        sub = content.split("Q")
        if len(sub) == 3:
            q = sub[1]
            a = sub[2]
            AUTO_REPLY[q] = a
            itchat.send('%s' % (WORD_ADD), msg['FromUserName'])
            return

    if  msg['Type'] == 'Text':
        if AUTO_REPLY.has_key(content):
            itchat.send('%s' % (AUTO_REPLY[content]), msg['FromUserName'])
            return

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
URL =  "http://192.168.200.28:8000/"
class loginCallBack:
    # uuid = None
    # def __init__(self,uuid):
    #     self.uuid = uuid

    def __call__(self,uuid = None , isLogin = None ,userName = None):
        url = URL + "bot/login/callback/"
        params = { 'uuid':123,'is_login':True,'user_name':userName}
        s = requests.Session()
        postQr = s.get(url, params=params)
        print postQr
        # Todo 登陆成功，同步 自动回复列表

        # print "back",uuid
        # url = "http://192.168.200.22:8000/bot/index/"
        # # qr = '%s/qrcode/%s' % (config.BASE_URL, uuid)
        #
        # # print "qr",qr
        # params = { 'uuid':uuid}
        #
        # self.s = requests.Session()
        # postQr = self.s.post(url, params=params)
        # print postQr
        # return True
            # if postQr:
            #     break
        # print "back"
# url = "http://192.168.200.22:8000/bot/login/callback/"
# params = { 'uuid':123,'is_login':True}
# s = requests.Session()
# # postQr = s.post(url, params=params)
# postQr = s.get(url, params=params)
# print postQr

# b()
    # url = "http://192.168.200.22:8000/bot/index/"
    # params = { 'uuid':self.uuid}
    # postQr = self.s.get(url, params=params)
# itchat.auto_login(hotReload=True,qrCallback=b)
    # itchat.auto_login(hotReload=True,uuid=uuid)

class Server():
    def __init__(self,uuid):
        self.uuid = uuid
    def updateReply(self):
        url = URL + "bot/update_reply/"
        params = { 'uuid':self.uuid,}
        s = requests.Session()
        postQr = s.get(url, params=params)
        print postQr
        print json.loads(postQr.text)
        return json.loads(postQr.text)

import sys
if __name__ == '__main__':
    print 'len',len(sys.argv),sys.argv

    #账号启动自带回复
    if len(sys.argv) == 3:
        print 2,sys.argv[2]
        # _reply_dict = json.loads(sys.argv[2])
        with open('E:\CarcerWorld\code\Python\git\image_str\image_server\wx_app\lib/robote/1.txt', "rb") as r:
            # _str = str(r.read()).replace("'", '"').replace("u", "")
            _str = str(r.read()).replace("'", '"')
            print _str
            _reply_dict = json.loads(_str)
            # _reply_dict = json.loads('{"1":"23"}')
            print _reply_dict

        AUTO_REPLY.clear()
        for i in _reply_dict:
            AUTO_REPLY[i] = _reply_dict[i]
    print AUTO_REPLY
    uuid = sys.argv[1]
    print 534543, uuid
    loginCall = loginCallBack()
    server = Server(uuid) # 与服务器通信

    itchat.auto_login(uuid=uuid,loginCallback=loginCall) #hack 做设置回调
    # itchat.auto_login(uuid=uuid)
    itchat.run()


