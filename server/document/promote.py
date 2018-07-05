#!/usr/bin/python
# -*- coding:utf-8 -*-
# author=hexm

from flask_restplus import fields
from server.status import APIStatus, FeedAPIStatus
from server import api

request_promote_effect_param = api.doc(params={
    'user_name': '用户名,默认:空',
    'mobile': '手机号,默认:空',
    'role_type': '推荐人角色,0:全部,1:货主,2:司机,3:物流公司,默认:0',
    'goods_type': '货源类型,0:全部,1:同城,2:跨城,默认:0',
    'is_actived': '是否活跃,0:全部,1:活跃(连续登录天数>1),2:一般(1-3天未登录),3:即将沉睡(4-10天未登录),4:沉睡(10天以上未登录),5:今天登录,默认:0',
    'is_car_sticker': '贴车贴,0:全部,1:有,2:无,默认:0',
    'start_time':'新增日期开始时间,默认:空',
    'end_time':'新增日期结束时间,默认:空',
    'page': '页数',
    'limit': '条数'
    }, description='推广统计列表查询参数')

response_promote_effect_param_success = response_success = api.response(200, '成功', api.model('response_success', {
    'state': fields.Integer(description=str(APIStatus.Ok)),
    'msg': fields.String(description=FeedAPIStatus.Decriptions[APIStatus.Ok]),
}))


request_promote_effect_add_param = api.doc(body=api.model('request_promote_effect_add', {
    'mobile': fields.String(description='手机号'),
    }, description='推广统计列表新增推广人员参数')
)

response_promote_effect_add_param_success = api.response(200, '成功', api.model('response_success', {
    'state': fields.Integer(description=str(APIStatus.Ok)),
    'msg': fields.String(description=FeedAPIStatus.Decriptions[APIStatus.Ok]),
}))

response_promote_effect_delete_param_success = api.response(200, '成功', api.model('response_success', {
    'state': fields.Integer(description=str(APIStatus.Ok)),
    'msg': fields.String(description=FeedAPIStatus.Decriptions[APIStatus.Ok]),
}))


request_promote_quality_param = api.doc(params={
    'start_time':'开始日期(时间戳),默认:8天前',
    'end_time':'结束日期(时间戳),默认:昨天',
    'periods':'时间周期,2:日，3:周，4:月，默认:2',
    'dimension':'统计维度,1:拉新,2:用户行为,3:金额,默认:1',
    'data_type':'数据类型,1,2,3...默认1',
    }, description='推广统计列表查询参数')

response_promote_quality_param_success = api.response(200, '成功', api.model('response_success', {
    'state': fields.Integer(description=str(APIStatus.Ok)),
    'msg': fields.String(description=FeedAPIStatus.Decriptions[APIStatus.Ok]),
}))
