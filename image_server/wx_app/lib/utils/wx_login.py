#coding:utf-8
import urllib2
from wx_app.models import *
from django.http import HttpResponse
import json,time
from django.db import transaction #事务

app_id = "wxff79e25befbb413d"
app_secret = "283fc3d9d4b8ba3b58601145466d4417"
def WxUserLogin(_js_code,_session):
	_expires = 1000000000 #session存活秒数
	# _js_code = request.GET['js_code']
	# _session = request.GET['session']

	_session_url = "https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code "  %(app_id,app_secret,_js_code )

	# if  _session == "false":  #像weixin查询openid,secret_key
	def WX_GetSession(_session_url):
		req = urllib2.Request(_session_url)
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
		response = opener.open(req)
		_json =  json.loads(response.read())
		return _json

	try:
		# raise NameError("There is a name error","in test.py")
		print "1:",_session
		if  User.objects.filter( session = _session ).exists() is False: #查session不存在,更新整个用户

			_json = WX_GetSession(_session_url)
			print _json
			if _json.has_key('errcode') : #登陆信息错误，结束
				return {"status":"false","msg":_json["errmsg"] }

			#查open_id存在user表中
			_expires_in =  time.time() + _json["expires_in"]  #存在时间
			_new_session = _js_code + str(time.time())
			_new_expires = time.time() + _expires

			if  User.objects.filter( wx_open_id =  _json["openid"] ).exists():
				_user = User.objects.get( wx_open_id =  _json["openid"] ) #用户存在，增加session
				_user.wx_session_key =  _json["session_key"]
				_user.wx_expires_in = _expires_in
				_user.session = _new_session
				_user.expires = _new_expires #当前时间+存活秒数
				_user.save()
				#登陆成功 ，返回session
				return {"status":"true","session":_new_session }
			else:
				with transaction.atomic(): #事务
					#不存在，新增用户
					_user = User(
						wx_open_id = _json["openid"],
						wx_session_key =  _json["session_key"],
						wx_expires_in = _expires_in,
						session = _new_session,
						expires = _new_expires,
					)
					_user.save()
					#新增默认目录
					_category = Category(
						name = u"默认目录",
						user_id = _user,
						is_default = 1,
					)
					_category.save()

					_id_list = [236]
					for i in _id_list:
						_img = Img.objects.get(id=i)
						_rel = RelCategoryImg(
							img=_img ,
							category = _category
						)
						_rel.save()
				#登陆成功 ，返回session
				return {"status":"true","session":_new_session }
		else : #session 存在，
			print "2:",_session
			_user = User.objects.get( session = _session )
			print _user
			if time.time() > _user.wx_expires_in : #wx_session 过期
				_json = WX_GetSession(_session_url)
				if _json["errcode"] : #登陆信息错误，结束
					return {"status":"false","msg":_json["errmsg"] }

				if _user.wx_open_id == _json["openid"]: #用户存在，跟新wx_session信息
					_user.wx_session_key = _json["session_key"]
					_user.wx_expires_in = time.time() + _json["expires_in"]
					_user.save()
				else:
					return {"status":"false","msg":"微信错误。未回复open_id" }

			if time.time() >_user.expires: # python 的session过期
				_new_session = _js_code + str(time.time())  #新的后台session
				_new_expires = time.time() + _expires #新的后台过期时间
				_user.session = _new_session
				_user.expires = _new_expires
				_user.save()
				return {"status":"true","session":_new_session }

			print _session
			#session未过期，回复继续使用
			return {"status":"true","session":_session }
	except Exception ,e:
		print e
		return {"status":"false","msg":u"用户登录错误"}

# if __name__ == "__main__":
# 	code = "051rqeXE0IKuwh2A9TZE0XFnXE0rqeXR"
# 	session = "051XgwH40A6C6H1U2dJ40G1zH40XgwHV1488348914.3"
# 	WxUserLogin(code,session)