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

		logo = request.GET['logo']
		title = request.GET['title']
		prize_url = request.GET['prize_url']
		is_gather_open = request.GET['is_gather_open']

		print user
		user['logo'] = logo
		user['title'] = title
		user['prize_url'] = prize_url
		user['is_gather_open'] = is_gather_open

		print user ,"OK"

		_dict = {
			"status":"true",
		}
		return HttpResponse(
			json.dumps({"status":"true"}),
			content_type="application/json"
		)


class GetUserInfo(ListView):
	def get(self, request, *args, **kwargs):
		_dict = {}
		return HttpResponse(
			json.dumps({"status":"true","user_info":user}),
			content_type="application/json"
		)


#获取发帖人的信息
class GetMasterInfo(ListView):
	def get(self, request, *args, **kwargs):
		master_session = request.GET['master_session']

		_dict = {}
		return HttpResponse(
			json.dumps({"status":"true","user_info":user}),
			content_type="application/json"
		)

#帮助发帖人
class HelpMaster(ListView):
	def get(self, request, *args, **kwargs):
		# todo
		# 将用户的图片， 绑定到master的名下
		# logo = request.GET['logo']
		# title = request.GET['title']
		# prize_url = request.GET['prize_url']
		# is_gather_open = request.GET['is_gather_open']
		#
		# print user
		# user['logo'] = logo
		# user['title'] = title
		# user['prize_url'] = prize_url
		# user['is_gather_open'] = is_gather_open

		print user ,"OK"

		_dict = {
			"status":"true",
		}
		return HttpResponse(
			json.dumps({"status":"true"}),
			content_type="application/json"
		)


