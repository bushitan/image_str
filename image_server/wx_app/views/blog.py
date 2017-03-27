#coding:utf-8
import urllib2
from django.http import HttpResponse
from wx_app.models import *
from django.views.generic import View, TemplateView, ListView, DetailView
import json


class EmojiArticleList(ListView):
    def get(self, request, *args, **kwargs):
		temp_list = Article.objects.filter()
		_art_list = []
		for i in range(0,len(temp_list)):
			_art_list.append({
				"art_id":temp_list[i].id,
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
		_dict = {
			"status":"true",
			"swiper": a.swiper.replace('\r\n','').split(",") , #轮播图
			"title":a.title,
			"art":_art,
			# "img_id":_img_id,
			# "category_id":_category_id,
		}
		return HttpResponse(
			json.dumps(_dict),
			content_type="application/json"
		)