# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404
import json
class Result():
    status = True
    code = 1
    def Success(self, *args, **kwargs):
        self.status = "true"
        return self.__Response(*args, **kwargs)

    def Problem(self, *args, **kwargs):
        self.status = "false"
        self.code = 3
        return self.__Response(*args, **kwargs)
    def Fail(self, *args, **kwargs):
        self.status = "false"
        self.code = 2
        return self.__Response(*args, **kwargs)

    def __Response(self, *args, **kwargs):
        r = {
            "status":self.status,
            "code":self.code,
        }
        for key in kwargs:
            r[key] = kwargs[key]
        return HttpResponse(json.dumps(r),content_type="application/json")
