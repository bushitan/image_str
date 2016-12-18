# -*- coding: utf-8 -*-
from django.contrib import admin
from wx_app.models import *

# Register your models here.

#history
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','name',)

class ImgAdmin(admin.ModelAdmin):
    list_display = ('name',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

class RelCategoryImgAdmin(admin.ModelAdmin):
    list_display = ('category','img')
    pass
class LogAdmin(admin.ModelAdmin):
    list_display = ('level','info','user','event')

admin.site.register(User,UserAdmin)
admin.site.register(Img,ImgAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(RelCategoryImg,RelCategoryImgAdmin)
admin.site.register(Log,LogAdmin)