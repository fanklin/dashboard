# -*- coding: utf-8 -*-
from flask_restful import abort

from server.database import db, mongo
from server.meta.decorators import make_decorator, Response
from server.models import RegionsModel
from server.models.promote import PromoteEffetList, PromoteQuality
from server.status import HTTPStatus, make_result, APIStatus


class PromoteEffectDecorator(object):

    @staticmethod
    @make_decorator
    def get_promote_effet_list(page, limit, params):
        data = PromoteEffetList.get_promote_effet_list(db.read_db, page, limit, params)

        return Response(data=data)


class PromoteQualityDecorator(object):

    @staticmethod
    @make_decorator
    def get_promote_quality(params):
        # 地区
        # user_id = []
        # if params['region_id']:
        #     three_region = RegionsModel.get_three_area(db.read_db, params['region_id'])
        #     if not three_region:
        #         abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='地区选择错误'))
        #     if three_region['first_code']:
        #         region = {
        #             'province_id': three_region['first_code'],
        #             'city_id': three_region['second_code'],
        #             'county_id': three_region['third_code']
        #         }
        #     else:
        #         region = {
        #             'province_id': three_region['second_code'],
        #             'city_id': three_region['third_code']
        #         }
        #     result = mongo.user_locations.collection.aggregate([{
        #         '$match': region
        #     },
        #         {'$group': {'_id': {'province_id': '$province_id', 'city_id': '$city_id', 'county_id': '$county_id'},
        #                     'scores': {'$addToSet': '$user_id'}}
        #          }])
        #     for i in result:
        #         user_id.extend(i['scores'])
        #     user_id = list(set(user_id))

        promote_quality = PromoteQuality.get_promote_quality(db.read_bi, params)

        return Response(params=params, data=promote_quality)
