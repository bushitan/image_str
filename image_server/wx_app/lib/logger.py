# -*- coding: utf-8 -*-
from wx_app.models import *
class Logger():
    def error(self,info,user,event):
        _log = Log(
            info = info,
            level = 3,
            event = event,
        )
        _log.save()
        return

    def log(self,info,user,event):
        _log = Log(
            info = info,
            level = 0,
            event = event,
        )
        _log.save()
    def info(self,**kwargs):
        return {
            "status":"false", #"true"
            "msg":"12321", #"true"
        }