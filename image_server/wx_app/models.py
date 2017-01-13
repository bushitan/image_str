# -*- coding: utf-8 -*-
from django.db import models

class string_with_title(str):
    """ 用来修改admin中显示的app名称,因为admin app 名称是用 str.title()显示的,
    所以修改str类的title方法就可以实现.
    """
    def __new__(cls, value, title):
        instance = str.__new__(cls, value)
        instance._title = title
        return instance

    def title(self):
        return self._title

    __copy__ = lambda self: self
    __deepcopy__ = lambda self, memodict: self

USER_ROLE = {
    0: u"普通用户",
    1: u'管理者'
}
CATEGORY_ROLE= {
    0: u"普通目录",
    1: u'默认目录'
}

LOG_LEVEL= {
    0: u"log",
    1: u'info',
    2: u'warm',
    3: u'error',
}

class User(models.Model):
    name =  models.CharField(max_length=100, verbose_name=u'名称',null=True,blank=True)
    wx_open_id = models.CharField(max_length=50, verbose_name=u'微信OpenID',null=True,blank=True)
    wx_session_key = models.CharField( max_length=128,verbose_name=u'微信SessionKey',null=True,blank=True)
    wx_expires_in = models.FloatField( verbose_name=u'微信SessionKey过期时间',null=True,blank=True)
    session = models.CharField (max_length=128, verbose_name=u'Django的session',null=True,blank=True)
    expires = models.FloatField( verbose_name=u'Django的session过期时间',null=True,blank=True)
    is_public = models.IntegerField(u'是否管理员',default=0,choices=USER_ROLE.items())
    uuid =  models.CharField(max_length=32, verbose_name=u'uuid标识',null=True,blank=True)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True,null=True,blank=True)
    class Meta:
        verbose_name_plural = verbose_name = u'用户'
        app_label = string_with_title('wx_app', u"表情")
    def __unicode__(self):
        return '%s' % (self.name)
class Img(models.Model):
    user_id = models.ForeignKey(User, verbose_name=u'用户',null=True,blank=True)
    name =  models.CharField(max_length=100, verbose_name=u'名称',null=True,blank=True)
    yun_url = models.TextField( verbose_name=u'云存储地址',null=True,blank=True)  #url 地址需要使用Text，用Char不显示，我也不懂为啥
    size = models.IntegerField(default=170,verbose_name='高x宽最大值')
    width =  models.IntegerField(default=0, verbose_name='宽',null=True,blank=True)
    height = models.IntegerField(default=0, verbose_name='高',null=True,blank=True)
    duration = models.FloatField(default=0, verbose_name='时长',null=True,blank=True)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True,null=True,blank=True)

    class Meta:
        verbose_name_plural = verbose_name = u'图片'
        ordering = ['-create_time']
        app_label = string_with_title('wx_app', u"表情")
    def __unicode__(self):
        return '%s' % (self.name)

class Category(models.Model):
    name =  models.CharField(max_length=100, verbose_name=u'名称',null=True,blank=True)
    user_id = models.ForeignKey(User, verbose_name=u'用户',null=True,blank=True)
    is_default = models.IntegerField(u'是否用户默认目录',default=0,choices=CATEGORY_ROLE.items(),)
    parent_id = models.ForeignKey('self', verbose_name=u'父类目录',null=True,blank=True)  #自身目录
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True,null=True,blank=True)
    class Meta:
        verbose_name_plural = verbose_name = u'目录'
        app_label = string_with_title('wx_app', u"表情")
    def __unicode__(self):
        return '%s' % (self.name)

class RelCategoryImg(models.Model):
    category = models.ForeignKey(Category, verbose_name=u'目录')
    img = models.ForeignKey(Img, verbose_name=u'图片')
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True,null=True,blank=True)
    class Meta:
        verbose_name_plural = verbose_name = u'目录图片关系'
        ordering = ['-create_time']
        app_label = string_with_title('wx_app', u"表情")

class Log(models.Model):
    info = models.CharField(max_length=100, verbose_name=u'信息',null=True,blank=True)
    user =  models.ForeignKey(User, verbose_name=u'用户',null=True,blank=True)
    level = models.IntegerField(u'信息等级',default=0,choices=LOG_LEVEL.items(),)
    event = models.CharField(max_length=100, verbose_name=u'所属事件',null=True,blank=True)
    occur_time = models.DateTimeField(u'发生时间', auto_now_add=True,blank=True)
    class Meta:
        verbose_name_plural = verbose_name = u'日志'
        app_label = string_with_title('wx_app', u"表情")
