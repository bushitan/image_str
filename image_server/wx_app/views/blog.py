#coding:utf-8
import urllib2
from django.http import HttpResponse
from wx_app.models import *
from django.views.generic import View, TemplateView, ListView, DetailView
import json

#查询文章列表
class EmojiArticleList(ListView):
	def get(self, request, *args, **kwargs):
		#用户点击“同款”标签记录
		user_log = UserLog(action = "same_list" )
		user_log.save()

		temp_list = Story.objects.filter()
		_art_list = []
		for i in range(0,len(temp_list)):
			if temp_list[i].is_show == 1:
				_art_list.append({
					"story_id":temp_list[i].id,
					"cover":temp_list[i].cover,
					"cover_style":temp_list[i].cover_style,
					# "swiper": temp_list[i].swiper.replace('\r\n','').split(","),
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

#获取文章具体内容
class EmojiBlog(ListView):
	def get(self, request, *args, **kwargs):
		# _art_id = request.GET['art_id']
		#
		# #用户浏览文章记录
		# user_log = UserLog(action = "same_view" ,data = str(_art_id) )
		# user_log.save()
		# print user_log.id
		# a = Article.objects.get(id = _art_id )
		# print a
		# _content_list = a.content.split("$")
		# # print b,len(b)
		# _art = []
		# for i in range(0,len(_content_list)):
		# 	if _content_list[i][0:4] == 'http':
		# 		_art.append({"style":"image","msg":_content_list[i]})
		# 	else:
		# 		_art.append({"style":"text","msg":_content_list[i]})
		#
		# print a.swiper.replace('\r\n','').split(",")
		# print "232" , a.content
		# _dict = {
		# 	"status":"true",
		# 	"swiper": a.swiper.replace('\r\n','').split(",") , #轮播图
		# 	"title":a.title,
		# 	"art":a.content,
		# 	# "tao_bao":eval(a.tao_bao),
		# 	# "img_id":_img_id,
		# 	# "category_id":_category_id,
		# }

		# _story_id = 1
		# _step_current = ""
		_story_id = request.GET.get('story_id',"")
		_step_current = request.GET.get('step_current',"")
		_tree = Story.objects.get(id = _story_id ).tree
		_tree_json =  json.loads(_tree)           #剧情树转json

		# print _current_art_id
		if _step_current == "":                        #从故事列表进入，步骤为空
			_current_art_id = _tree_json.keys()[0] #获取当前文章的id
			_art_list = [_current_art_id]           #第一步为用户已经走的路
		else:
			_art_list = _step_current.split(',')
			_current_art_id = _art_list[-1]         #最新的步数为当前浏览步数
		# print _art_list
		_step_next = {}     #设置下一步信息你
		temp = _tree_json
		for item in _art_list: #遍历步骤列表
			temp=temp[item]
			if item == _art_list[-1]: #根据步骤，获取当前步数的son
				key_list = ["right_id", "right_name","left_id","left_name"]
				for k in key_list:    #将son的左右数据，依次存入_step_next
					if temp.has_key(k):
						_step_next[k] = temp[k]

		a = Article.objects.get(id = _current_art_id )  #当前步数对应的文章

		_dict = {
			"status":"true",
			"swiper": a.swiper.replace('\r\n','').split(",") , #轮播图
			"title":a.title,
			"content":a.content,
			"step_current":','.join(_art_list),
			"step_next":_step_next,
		}
		print _dict
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
