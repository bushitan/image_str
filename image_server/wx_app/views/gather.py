# -*- coding: utf-8 -*-
from django.http import HttpResponse
from wx_app.models import *
from django.views.generic import View, TemplateView, ListView, DetailView
import json
import image_server.settings as SETTING

user = {
	'session':"",
	'logo':"http://img.12xiong.top/help_logo.png",
	'title':'第一个主题',
	'prize_url':'../../images/help_tie_qr.jpg',
	'is_gather_open':1,
}

M_LOGO = "http://img.12xiong.top/help_logo.png"
M_QR_HOST = "http://img.12xiong.top/master/"
M_NICK_NAME = u"好玩的名字"
M_TITLE = u"搞笑的图片"
M_PRIZE_URL = "http://img.12xiong.top/help_img.png"


#设置英雄帖用户信息
class SetMUserInfo(ListView):
	def get(self, request, *args, **kwargs):
		session = request.GET.get('session',"")
		logo = request.GET.get('logo',"")
		nick_name = request.GET.get('nick_name',"")
		title =request.GET.get('title',"")
		prize_url = request.GET.get('prize_url',"")
		is_gather_open = int(request.GET.get('is_gather_open',""))
		print session,type(title)
		print logo,
		print title,type(title)
		print prize_url
		print is_gather_open,type(is_gather_open)
		if  User.objects.filter( session = session).exists() is False:
			return HttpResponse( json.dumps({"status":"false","msg":u"用户不存在,请重新登录"}),content_type="application/json" )
		_user = User.objects.get( session = session)
		#bug 用save方式，会把字符串变tuple保存
		#filter有update，get没有
		Master.objects.filter(user = _user).update(
			logo_url = logo,
			nick_name = nick_name,
			title = title,
			prize_url = prize_url,
			is_gather_open = is_gather_open,
		)
		# _dict = {
		# 	"status":"true",
		# }
		return HttpResponse(
			json.dumps({"status":"true"}),
			content_type="application/json"
		)


class GetMUserInfo(ListView):
	def get(self, request, *args, **kwargs):
		session = request.GET.get('session',"")
		print ' in GetUserInfo ',session
		# return HttpResponse(
		# 	json.dumps({"status":"true"}),
		# 	content_type="application/json"
		# )
		if  User.objects.filter( session = session).exists() is False:
			return HttpResponse( json.dumps({"status":"false","msg":u"用户不存在,请重新登录"}),content_type="application/json" )
		_user = User.objects.get( session = session)
		if  Master.objects.filter( user = _user).exists() is False: #新注册master
			_master = Master(user = _user)
			_master.save()
			_master_info = {
				'master_id':_master.id,
				"nick_name":M_NICK_NAME if _master.nick_name =="" else _master.nick_name,
				'logo': M_LOGO if _master.logo_url =="" else _master.logo_url,
				'title': M_TITLE if _master.title =="" else _master.title,
				'qr_url':M_QR_HOST + str(_master.id) +".jpg",
				'prize_url':M_PRIZE_URL if _master.prize_url =="" else _master.prize_url,
				'is_gather_open':_master.is_gather_open,
			}
			print 'M_LOGO',  M_LOGO if _master.logo_url is None else _master.logo_url
			return HttpResponse( json.dumps({"status":"true","master_info":_master_info,"rel_master_img":[]}),content_type="application/json" )
		else: #master已经有，查询
			_master = Master.objects.get(user = _user)
			print ' in GetUserInfo have',_master.title
			_master_info = { #查信息
				'master_id':_master.id,
				"nick_name":M_NICK_NAME if _master.nick_name =="" else _master.nick_name,
				'logo': M_LOGO if _master.logo_url =="" else _master.logo_url,
				'title': M_TITLE if _master.title =="" else _master.title,
				'qr_url':M_QR_HOST + str(_master.id) +".jpg",
				'prize_url':M_PRIZE_URL if _master.prize_url =="" else _master.prize_url,
				'is_gather_open':_master.is_gather_open,
			}
			print 'M_LOGO',  M_LOGO if _master.logo_url is None else _master.logo_url
			print _master_info

			_rel = RelMasterUserImg.objects.filter(user = _user) #查图片
			_img_list = []
			for _r in _rel:
				_img_list.append({
					"img_id":_r.img.id,
					"yun_url":_r.img.yun_url, # 七牛云自动缩略图
					"size":_r.img.size ,
					"width":_r.img.width,
					"height":_r.img.height,
					"duration":_r.img.duration,
				})
		return HttpResponse(
			json.dumps({"status":"true","master_info":_master_info,"img_list":_img_list,}),
			content_type="application/json"
		)


#获取发帖人的信息
class GetMasterInfo(ListView):
	def get(self, request, *args, **kwargs):
		# master_id = request.GET['master_id']
		master_id = request.GET.get('master_id',"")
		# if Master.objects.filter( id = master_id).exists() is False:
		# 	return HttpResponse( json.dumps({"status":"false","msg":u"master用户不存在,请重新登录"}),content_type="application/json" )
	 	_master = Master.objects.get( id = master_id)
		_master_info = {
			"nick_name":M_NICK_NAME if _master.nick_name == ""  else _master.nick_name,
			'logo': M_LOGO if _master.logo_url == ""  else _master.logo_url,
			'title': M_TITLE if _master.title  == ""  else _master.title,
			'prize_url':M_PRIZE_URL if _master.prize_url  == ""  else _master.prize_url,
			'is_gather_open':_master.is_gather_open,
		}
		return HttpResponse(
			json.dumps({"status":"true","master_info":_master_info}),
			content_type="application/json"
		)

#帮助发帖人
class HelpMaster(ListView):
	def get(self, request, *args, **kwargs):

		master_id = request.GET.get('master_id',"")
		img_id = request.GET.get('img_id',"")

		master = Master.objects.get(id = master_id)
		rel = RelMasterUserImg(user = master.user ,img_id = img_id )
		rel.save()
		_dict = {
			"status":"true",
		}
		return HttpResponse(
			json.dumps({"status":"true"}),
			content_type="application/json"
		)

import  urllib2,urllib
import time
TIME_OUT = {
	'ACCESS_TOKEN':'',
	'NOW':1,
	'END':0,
}
class CreateMasterQR(ListView):
	def get(self, request, *args, **kwargs):
		# pass
		# todo
		# print user ,"OK"
		#
		# print TIME_OUT
		TIME_OUT['NOW'] = time.time()
		if  TIME_OUT['NOW']  > TIME_OUT['END'] :
			wx_token_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' %( SETTING.APP_ID,SETTING.APP_SECRET)
			# print wx_token_url
			req = urllib2.Request(wx_token_url)
			opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
			response = opener.open(req)
			wx_toekn =  json.loads(response.read())
			TIME_OUT['ACCESS_TOKEN'] =  wx_toekn["access_token"]
			TIME_OUT['END'] =  TIME_OUT['NOW'] + wx_toekn["expires_in"]


		#获取二维码
		# print TIME_OUT['ACCESS_TOKEN']
		url = 'http://api.weixin.qq.com/wxa/getwxacodeunlimit?access_token=%s' % ( TIME_OUT['ACCESS_TOKEN'])
		data = {
			'scene': '2',
			'width': 430,
			'auto_color':False,
			'line_color':{"r":"0","g":"0","b":"0"}
		}
		headers = {'Content-Type': 'application/json'}
		request = urllib2.Request(url=url, headers=headers, data=json.dumps(data))
		response = urllib2.urlopen(request)
		# print response.read()
		local=open('D:/tmp.jpg','wb')
		local.write(response.read())
		local.close()

		_dict = {
			"status":"true",
		}
		return HttpResponse(
			json.dumps({"status":"true"}),
			content_type="application/json"
		)

	def post(self, request, *args, **kwargs):

		a = request.GET.get('a',"")
		b = request.POST.get('img_url',"")
		print a ,b
		return HttpResponse(
			json.dumps({"status":"post true"}),
			content_type="application/json"
		)