#coding:utf-8
import urllib2
from django.http import HttpResponse
from wx_app.models import *
from django.views.generic import View, TemplateView, ListView, DetailView
import json


class EmojiArticleList(ListView):
	def get(self, request, *args, **kwargs):
		#用户点击“同款”标签记录
		user_log = UserLog(action = "same_list" )
		user_log.save()

		temp_list = Article.objects.filter()
		_art_list = []
		for i in range(0,len(temp_list)):
			if temp_list[i].is_show == 1:
				_art_list.append({
					"art_id":temp_list[i].id,
					"cover":temp_list[i].cover,
					"swiper": temp_list[i].swiper.replace('\r\n','').split(","),
					"title":temp_list[i].title,
					"summary":temp_list[i].summary
				})
		_dict = {
			"status":"true",
			"art_list":_art_list,
		}
		return HttpResponse(
			json.dumps(_dict),
			content_type="application/json"
		)
class EmojiBlog(ListView):
	def get(self, request, *args, **kwargs):
		_art_id = request.GET['art_id']

		#用户浏览文章记录
		user_log = UserLog(action = "same_view" ,data = str(_art_id) )
		user_log.save()
		print user_log.id
		a = Article.objects.get(id = _art_id )
		print a
		_content_list = a.content.split("$")
		# print b,len(b)
		_art = []
		for i in range(0,len(_content_list)):
			if _content_list[i][0:4] == 'http':
				_art.append({"style":"image","msg":_content_list[i]})
			else:
				_art.append({"style":"text","msg":_content_list[i]})

		print a.swiper.replace('\r\n','').split(",")
		print "232" , a.tao_bao
		_dict = {
			"status":"true",
			"swiper": a.swiper.replace('\r\n','').split(",") , #轮播图
			"title":a.title,
			"art":_art,
			"tao_bao":eval(a.tao_bao),
			# "img_id":_img_id,
			# "category_id":_category_id,
		}
		return HttpResponse(
			json.dumps(_dict),
			content_type="application/json"
		)

import xlrd
class Taobao(ListView):
	def get(self, request, *args, **kwargs):
		_dict = {}
		return HttpResponse(
			json.dumps(_dict),
			content_type="application/json"
		)

		# _art_id = request.GET['art_id']
		data = xlrd.open_workbook('2.xls') # 打开xls文件
		table = data.sheets()[0] # 打开第一张表
		nrows = table.nrows # 获取表的行数
		print nrows
