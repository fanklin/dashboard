#!/usr/bin/python
# -*- coding:utf-8 -*-
# author=hexm

from flask_restplus.resource import Resource

import server.document.root as doc
from server import api
from server import verify, operations, filters
from server.meta.decorators import Response
from server.meta.session_operation import sessionOperationClass
from server.utils.request import *


class RootManagement(Resource):
    @staticmethod
    @doc.request_root_management_get
    @filters.RootManagement.get_result(data=dict)
    @operations.RootManagement.get_data(params=dict)
    @verify.RootManagement.check_get_params(params=dict)
    def get():
        """获取用户管理列表"""
        if sessionOperationClass.check():
            role, _ = sessionOperationClass.get_role()
            if role == '超级管理员':
                resp = Response(params=get_all_arg())
                return resp
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.Forbidden, msg='仅限后台用户获取账户列表'))
        abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.UnLogin, msg='未登录用户'))

    @staticmethod
    @doc.request_root_management_add
    @operations.RootManagement.post_data(params=dict)
    @verify.RootManagement.check_post_params(params=dict)
    def post():
        """增加新的用户"""
        if sessionOperationClass.check():
            role, _ = sessionOperationClass.get_role()
            if role == '超级管理员':
                resp = Response(params=get_payload())
                return resp
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.Forbidden, msg='仅限超级管理员添加账户'))
        abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.UnLogin, msg='未登录用户'))


class RootManagementOperator(Resource):
    @staticmethod
    @operations.RootManagement.delete_data(params=dict)
    def delete(admin_id):
        """删除该账户"""
        if sessionOperationClass.check():
            role, _ = sessionOperationClass.get_role()
            if role == '超级管理员':
                return Response(params={'admin_id': admin_id})
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.Forbidden, msg='仅限超级管理员删除账户'))
        abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.UnLogin, msg='未登录用户'))

    @staticmethod
    @doc.request_root_management_put
    @operations.RootManagement.put_data(params=dict)
    @verify.RootManagement.check_put_params(params=dict)
    def put(admin_id):
        """修改当前用户id的账号或者密码"""
        if sessionOperationClass.check():
            role, _ = sessionOperationClass.get_role()
            if role == '超级管理员':
                if admin_id == 0:
                    abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.Forbidden, msg='用户id不能为0'))
                params = get_payload()
                params.setdefault('admin_id', admin_id)
                return Response(params=params)
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.Forbidden, msg='仅限超级管理员修改账户'))
        abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.UnLogin, msg='未登录用户'))

    @staticmethod
    @operations.RootManagement.get_role(admin_id=int)
    def get(admin_id):
        """获取当前用户所有角色"""
        if sessionOperationClass.check():
            role, _ = sessionOperationClass.get_role()
            if role == '超级管理员':
                resp = Response(admin_id=int(admin_id))
                return resp
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.Forbidden, msg='仅限后台用户获取账户列表'))
        abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.UnLogin, msg='未登录用户'))


class RootRoleManagement(Resource):
    @staticmethod
    @doc.request_root_management_get
    @filters.RootRoleManagement.get_result(data=dict)
    @operations.RootRoleManagement.get_role_list(params=dict)
    @verify.RootManagement.check_get_params(params=dict)
    def get():
        """获取所有角色的列表"""
        if sessionOperationClass.check():
            role, _ = sessionOperationClass.get_role()
            if role == '超级管理员':
                resp = Response(params=get_all_arg())
                return resp
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.Forbidden, msg='仅限后台用户获取角色列表'))
        abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.UnLogin, msg='未登录用户'))

    @staticmethod
    @doc.request_root_role_management_add
    @operations.RootRoleManagement.post_data(params=dict)
    @verify.RootRoleManagement.check_post_params(params=dict)
    def post():
        """新增一个角色"""
        if sessionOperationClass.check():
            role, _ = sessionOperationClass.get_role()
            if role == '超级管理员':
                resp = Response(params=get_payload())
                return resp
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.Forbidden, msg='仅限后台用户新增角色列表'))
        abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.UnLogin, msg='未登录用户'))


class RootRoleManagementOperator(Resource):

    @staticmethod
    @doc.request_root_management_put
    @operations.RootRoleManagement.put_data(params=dict)
    @verify.RootRoleManagement.check_put_params(params=dict)
    def put(role_id):
        """修改当前角色的名称,地区权限,页面权限"""
        if sessionOperationClass.check():
            role, _ = sessionOperationClass.get_role()
            if role == '超级管理员':
                if role_id == 0:
                    abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.Forbidden, msg='角色id不能为0'))
                params = get_payload()
                params.setdefault('role_id', role_id)
                return Response(params=params)
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.Forbidden, msg='仅限超级管理员修改角色'))
        abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.UnLogin, msg='未登录用户'))

    @staticmethod
    def delete(role_id):
        """删除当前角色"""
        pass


ns = api.namespace('root', description='用户管理')
ns.add_resource(RootManagement, '/management/')
ns.add_resource(RootManagementOperator, '/management/<int:admin_id>')
ns.add_resource(RootRoleManagement, '/role_management/')
ns.add_resource(RootRoleManagementOperator, '/role_management/<int:role_id>')
