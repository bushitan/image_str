# -*- coding: utf-8 -*-
from wx_app.models import *

class Login():
    def SessionExists(self,session):
        return User.objects.filter( session = session).exists()

    def GetUser(self,session):
        return User.objects.get( session = session)
# def LoginFactory():
#     login = Login()
#     return login