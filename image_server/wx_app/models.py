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

class User(models.Model):
    name =  models.CharField(max_length=100, verbose_name=u'名称',null=True)
    wx_open_id = models.CharField(max_length=50, verbose_name=u'微信OpenID',null=True)
    wx_session_key = models.CharField( max_length=128,verbose_name=u'微信SessionKey',null=True)
    wx_expires_in = models.FloatField( verbose_name=u'微信SessionKey过期时间',null=True)
    session = models.CharField (max_length=128, verbose_name=u'Django的session',null=True)
    expires = models.FloatField( verbose_name=u'Django的session过期时间',null=True)

    is_public = models.IntegerField(u'是否管理员',default=0,choices=USER_ROLE.items())
    uuid =  models.CharField(max_length=32, verbose_name=u'uuid标识',null=True)
    class Meta:
        verbose_name_plural = verbose_name = u'用户'
        app_label = string_with_title('wx_app', u"表情")
    def __unicode__(self):
        return '%s' % (self.name)
class Img(models.Model):
    name =  models.CharField(max_length=100, verbose_name=u'名称',null=True,)
    yun_url = models.TextField( verbose_name=u'云存储地址',null=True)  #url 地址需要使用Text，用Char不显示，我也不懂为啥
    size = models.IntegerField(default=170,verbose_name='高x宽最大值')
    # height = models.IntegerField(default=170, verbose_name='高')
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)

    class Meta:
        verbose_name_plural = verbose_name = u'图片'
        app_label = string_with_title('wx_app', u"表情")
    def __unicode__(self):
        return '%s' % (self.name)

class Category(models.Model):
    name =  models.CharField(max_length=100, verbose_name=u'名称',null=True,)
    user_id = models.ForeignKey(User, verbose_name=u'用户')
    is_default = models.IntegerField(u'是否用户默认目录',default=0,choices=CATEGORY_ROLE.items(),)
    parent_id = models.OneToOneField('self', verbose_name=u'父类目录',null=True,)  #自身目录
    class Meta:
        verbose_name_plural = verbose_name = u'目录'
        app_label = string_with_title('wx_app', u"表情")
    def __unicode__(self):
        return '%s' % (self.name)

class RelCategoryImg(models.Model):
    category = models.ForeignKey(Category, verbose_name=u'目录')
    img = models.ForeignKey(Img, verbose_name=u'图片')
    class Meta:
        verbose_name_plural = verbose_name = u'目录图片关系'
        app_label = string_with_title('wx_app', u"表情")

