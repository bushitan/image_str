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

STEP_FREE = {
    0:u"空闲，可下一步",
    1:u"非空闲，不能下一步",
}
THEME_LIFT = {
    0:u"激活",
    1:u"不激活",
    2:u"删除",
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
    fsize =  models.IntegerField(default=0, verbose_name='文件大小',null=True,blank=True)
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
    des = models.TextField( verbose_name=u'描述',null=True,blank=True)
    user_id = models.ForeignKey(User, verbose_name=u'用户',null=True,blank=True)
    is_default = models.IntegerField(u'是否用户默认目录',default=0,choices=CATEGORY_ROLE.items(),)
    sn = models.IntegerField(u'排序号',default=0,null=True,blank=True)
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


GATHER_OPEN = {
    0:u"关闭，不接受求图",
    1:u"打开，可以求图",
}
#Master的信息
class Master(models.Model):
    user= models.ForeignKey(User, verbose_name=u'master用户',null=True,blank=True)
    nick_name = models.CharField(max_length=32, verbose_name=u'昵称',default="",null=True,blank=True)
    title = models.CharField(max_length=100, verbose_name=u'标题',default="",null=True,blank=True)
    # qr_url = models.CharField(max_length=100, verbose_name=u'二维码图片',null=True,blank=True)
    logo_url = models.TextField( verbose_name=u'头像icon',default="",null=True,blank=True)
    prize_url = models.TextField( verbose_name=u'奖励图片',default="",null=True,blank=True)
    is_gather_open = models.IntegerField(u'是否接受求图',default=1,choices=GATHER_OPEN.items(),)
    class Meta:
        verbose_name_plural = verbose_name = u'发帖者'
        app_label = string_with_title('wx_app', u"表情")
#Master的收集表
class RelMasterUserImg(models.Model):
    user= models.ForeignKey(User, verbose_name=u'master用户',null=True,blank=True)
    img = models.ForeignKey(Img, verbose_name=u'收到图片')
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True,null=True,blank=True)
    class Meta:
        verbose_name_plural = verbose_name = u'匿名回复图片'
        ordering = ['-create_time']
        app_label = string_with_title('wx_app', u"表情")

#一起画

#主题
class Theme(models.Model):
    name =  models.CharField(max_length=100, verbose_name=u'名称',null=True,blank=True)
    user_id = models.ForeignKey(User, verbose_name=u'发起用户',null=True,blank=True)
    # sn =  models.CharField(max_length=32, verbose_name=u'主题序列号',null=True,blank=True)
    lift =  models.IntegerField(u'生命周期',default=0,choices=THEME_LIFT.items(),)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True,null=True,blank=True)
    class Meta:
        verbose_name_plural = verbose_name = u'绘画主题'
        app_label = string_with_title('wx_app', u"表情")
    def __unicode__(self):
        return '%s' % (self.name)

#主题与参与用户记录，用户查询自己参与的所有主题
class RelThemeUser(models.Model):
    theme = models.ForeignKey(Theme, verbose_name=u'主题')
    user = models.ForeignKey(User, verbose_name=u'参与用户')
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True,null=True,blank=True)
    class Meta:
        verbose_name_plural = verbose_name = u'绘画主题与参与用户关系'
        ordering = ['-create_time']
        app_label = string_with_title('wx_app', u"表情")

#绘画步骤，1个主题对应多个步骤
# 创立之初，用户为空，用户可抢，用户填上；其他则不可抢
class Step(models.Model):
    theme_id = models.ForeignKey(Theme, verbose_name=u'主题',null=True,blank=True)
    user_id = models.ForeignKey(User, verbose_name=u'参与用户',null=True,blank=True)
    # img_id = models.ForeignKey(Img, verbose_name=u'图片',null=True,blank=True)
    img_url = models.TextField( verbose_name=u'图片地址',null=True,blank=True)  #直接对应图片地址，避免Img误删，做删除联合查询
    number = models.IntegerField(u'步数',default=1,null=True,blank=True)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True,null=True,blank=True)
    next_user =  models.IntegerField( verbose_name=u'下一个用户',null=True,blank=True)
    # next_user =  models.ForeignKey(User, verbose_name=u'下一个用户',null=True,blank=True)
    # is_free  = models.IntegerField(u'是否可抢',default=0,choices=STEP_FREE.items(),)
    # name =  models.CharField(max_length=100, verbose_name=u'名称',null=True,blank=True)
    # key =  models.CharField(max_length=32, verbose_name=u'步骤标记',null=True,blank=True)

    class Meta:
        verbose_name_plural = verbose_name = u'绘画步骤'
        app_label = string_with_title('wx_app', u"表情")
        ordering = ['-create_time']
        get_latest_by = 'create_time'
    def __unicode__(self):
        return '%s' % (self.number)


ARTICLE_SHOW = {
    1:u"显示",
    0:u"隐藏",
}
COVER_STYLE = {
    0:u"图片",
    1:u"视频",
}
class Article(models.Model):
    cover = models.CharField(max_length=100, verbose_name=u'封面图片',null=True,blank=True)
    cover_style = models.IntegerField(u'封面类型',default=0,choices=COVER_STYLE.items())
    title = models.CharField(max_length=100, verbose_name=u'标题',null=True,blank=True)
    swiper = models.CharField(max_length=200, verbose_name=u'轮播图',null=True,blank=True)
    summary = models.CharField(max_length=100,verbose_name=u'摘要',null=True,blank=True)
    content = models.TextField(verbose_name=u'正文',null=True,blank=True)
    is_show = models.IntegerField(u'是否显示文章',default=1,choices=ARTICLE_SHOW.items(),)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    # tao_bao = models.CharField(max_length=100,verbose_name=u'淘宝链接',null=True,blank=True)
    def get_tags(self):
        return self.tags.split(',')

    class Meta:
        verbose_name_plural = verbose_name = u'文章'
        ordering = ['-create_time']
        # ordering = ['rank', '-is_top', '-pub_time', '-create_time']
        app_label = string_with_title('wx_app', u"表情")

    def __unicode__(self):
            return self.title

class Story(models.Model):
    name = models.CharField(max_length=32, verbose_name=u'故事名字',null=True,blank=True)
    tree = models.TextField(verbose_name=u'剧情树',null=True,blank=True)
    cover = models.CharField(max_length=100, verbose_name=u'封面图片',null=True,blank=True)
    cover_style = models.IntegerField(u'封面类型',default=0,choices=COVER_STYLE.items())
    title = models.CharField(max_length=100, verbose_name=u'标题',null=True,blank=True)
    summary = models.CharField(max_length=100,verbose_name=u'摘要',null=True,blank=True)
    is_show = models.IntegerField(u'是否显示文章',default=1,choices=ARTICLE_SHOW.items(),)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True,null=True,blank=True)
    class Meta:
        verbose_name_plural = verbose_name = u'故事剧情'
        ordering = ['-create_time']
        # ordering = ['rank', '-is_top', '-pub_time', '-create_time']
        app_label = string_with_title('wx_app', u"表情")
    def __unicode__(self):
            return self.name

class UserBack(models.Model):
    user = models.ForeignKey(User, verbose_name=u'用户',null=True,blank=True)
    back = models.TextField(verbose_name=u'反馈信息',null=True,blank=True)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    class Meta:
        verbose_name_plural = verbose_name = u'用户反馈'
        ordering = ['-create_time']
        # ordering = ['rank', '-is_top', '-pub_time', '-create_time']
        app_label = string_with_title('wx_app', u"表情")

    def __unicode__(self):
            return self.back

class UserLog(models.Model):
    user = models.ForeignKey(User, verbose_name=u'用户',null=True,blank=True)
    action = models.CharField(max_length=32, verbose_name=u'动作',null=True,blank=True)
    data = models.CharField(max_length=32, verbose_name=u'数据',null=True,blank=True)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    class Meta:
        verbose_name_plural = verbose_name = u'用户浏览记录'
        ordering = ['-create_time']
        # ordering = ['rank', '-is_top', '-pub_time', '-create_time']
        app_label = string_with_title('wx_app', u"表情")

    def __unicode__(self):
            return self.action
