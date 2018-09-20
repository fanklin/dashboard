# -*- coding: utf-8 -*-

from server.meta.decorators import make_decorator
from server.status import HTTPStatus, APIStatus, make_resp

class Weather(object):

    @staticmethod
    @make_decorator
    def get_result(data):
        return make_resp(APIStatus.Ok, data=data), HTTPStatus.Ok
