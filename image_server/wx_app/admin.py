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
    list_display = ('id','name','parent_id','user_id','sn')
    search_fields = ('user_id__name',)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent_id":
            kwargs["queryset"] = Category.objects.filter(user_id = 2)
        return super(CategoryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

class RelCategoryImgAdmin(admin.ModelAdmin):
    list_display = ('id','category_id','img_id','create_time',)
    search_fields = ('category__name',)
    pass
class LogAdmin(admin.ModelAdmin):
    list_display = ('id','level','info','user','event')
admin.site.register(User,UserAdmin)
admin.site.register(Img,ImgAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(RelCategoryImg,RelCategoryImgAdmin)
admin.site.register(Log,LogAdmin)

# gahter 英雄帖
class RelMasterUserImgAdmin(admin.ModelAdmin):
    list_display = ('id','user_id','img_id','create_time',)
admin.site.register(RelMasterUserImg,RelMasterUserImgAdmin)
class MasterAdmin(admin.ModelAdmin):
    list_display = ('id','user_id','title','logo_url','prize_url','is_gather_open',)
admin.site.register(Master,MasterAdmin)

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


class StoryAdmin(admin.ModelAdmin):
    list_display = ('id','name',)
admin.site.register(Story,StoryAdmin)
class ArticleAdmin(admin.ModelAdmin):
    # formfield_overrides = {models.TextField: {'widget': form.Textarea},}
    # class Media:
    #     js = (
    #         '/static/tinymce/tinymce.min.js',
    #         '/static/tinymce/textareas.js',
    #     )
    list_display = ('id','title','content',)
    class Media:
        js = ('/static/tinymce/tinymce.min.js',
              '/static/tinymce/textareas.js')
    fieldsets = (
        # (u'基本信息', {
        #     'fields': ('title', 'en_title', 'img'
        #                , 'tags',
        #                'is_top', 'rank')
        #     }),
        # (u'内容', {
        #     'fields': ('content',)
        #     }),
        # (u'摘要', {
        #     'fields': ('summary',)
        #     }),
        # (u'时间', {
        #     'fields': ('pub_time',)
        #     }),
    )
    # class Media:
    #     js=("//tinymce.cachefly.net/4.0/tinymce.min.js","/static/js/edit.js")

admin.site.register(Article,ArticleAdmin)


class UserBackAdmin(admin.ModelAdmin):
    list_display = ('user','back',)
admin.site.register(UserBack,UserBackAdmin)


class UserLogAdmin(admin.ModelAdmin):
    list_display = ('user','action','data',)
admin.site.register(UserLog,UserLogAdmin)