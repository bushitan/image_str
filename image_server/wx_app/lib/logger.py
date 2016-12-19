# -*- coding: utf-8 -*-
from wx_app.models import *
class Logger():
    def error(self,info,user,event):
        _log = Log(
            info = info,
            user =  user,
            level = 3,
            event = event,
        )
        _log.save()
        return

    def info(self,**kwargs):

        return {
            "status":"false", #"true"
            "msg":"12321", #"true"
        }