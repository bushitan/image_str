# -*- coding: utf-8 -*-
from django.http import HttpResponse
from wx_app.models import *
from django.views.generic import View, TemplateView, ListView, DetailView
import json

user = {
	'session':"",
	'logo':"../../images/cartHL.png",
	'title':'第一个主题',
	'prize_url':'../../images/help_tie_qr.jpg',
	'is_gather_open':1,
}

#设置英雄帖用户信息
class SetUserInfo(ListView):
	def get(self, request, *args, **kwargs):

		session = request.GET['session']
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


class GetUserInfo(ListView):
	def get(self, request, *args, **kwargs):
		session = request.GET['session']
		print ' in GetUserInfo ',session
		if  User.objects.filter( session = session).exists() is False:
			return HttpResponse( json.dumps({"status":"false","msg":u"用户不存在,请重新登录"}),content_type="application/json" )
		_user = User.objects.get( session = session)
		if  Master.objects.filter( user = _user).exists() is False: #新注册master
			_master = Master(user = _user)
			_master.save()
			_master_info = {
				"nick_name":u'丰兄',
				'logo':_master.logo_url,
				'title':_master.title,
				'prize_url':_master.prize_url,
				'is_gather_open':_master.is_gather_open,
			}
			return HttpResponse( json.dumps({"status":"true","master_info":_master_info,"rel_master_img":[]}),content_type="application/json" )
		else: #master已经有，查询
			_master = Master.objects.get(user = _user)
			_master_info = { #查信息
				"nick_name":u'丰兄',
				'logo':_master.logo_url,
				'title':_master.title,
				'prize_url':_master.prize_url,
				'is_gather_open':_master.is_gather_open,
			}

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
		master_id = request.GET['master_id']
		# if Master.objects.filter( id = master_id).exists() is False:
		# 	return HttpResponse( json.dumps({"status":"false","msg":u"master用户不存在,请重新登录"}),content_type="application/json" )
	 	_master = Master.objects.get( id = master_id)
		_master_info = {
			"nick_name":u'丰兄',
			'logo':_master.logo_url,
			'title':_master.title,
			'prize_url':_master.prize_url,
			'is_gather_open':_master.is_gather_open,
		}
		return HttpResponse(
			json.dumps({"status":"true","master_info":_master_info}),
			content_type="application/json"
		)

#帮助发帖人
class HelpMaster(ListView):
	def get(self, request, *args, **kwargs):
		pass
		# todo
		# print user ,"OK"
		#
		# _dict = {
		# 	"status":"true",
		# }
		# return HttpResponse(
		# 	json.dumps({"status":"true"}),
		# 	content_type="application/json"
		# )


