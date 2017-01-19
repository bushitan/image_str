# -*- coding: utf-8 -*-
from django.contrib import admin
from wx_app.models import *

# Register your models here.

#history
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','name',)

class ImgAdmin(admin.ModelAdmin):
    list_display = ('id','name','user_id')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name','user_id')

class RelCategoryImgAdmin(admin.ModelAdmin):
    list_display = ('category_id','img_id')
    pass
class LogAdmin(admin.ModelAdmin):
    list_display = ('level','info','user','event')
admin.site.register(User,UserAdmin)
admin.site.register(Img,ImgAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(RelCategoryImg,RelCategoryImgAdmin)
admin.site.register(Log,LogAdmin)

#一起画
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('id','name','user_id')
class RelThemeUserAdmin(admin.ModelAdmin):
    list_display = ('id','theme_id','user_id')
class StepAdmin(admin.ModelAdmin):
    list_display = ('id','number',"next_user",'theme_id','img_url','user_id')

admin.site.register(Theme,ThemeAdmin)
admin.site.register(RelThemeUser,RelThemeUserAdmin)
admin.site.register(Step,StepAdmin)


