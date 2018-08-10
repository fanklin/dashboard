# -*- coding: utf-8 -*-
import re
from threading import Lock

from flask import render_template, session, redirect

from server import app
from server.cache_data import init_regions
from server.database import db
from server.meta.login_record import visitor_record
from server.meta.session_operation import sessionOperationClass
from server.models.long_term_vehicle import LongTermVehiclModel
from server.models.message import MessageSystemModel

thread = None
thread_lock = Lock()


@app.route('/message/', endpoint='message')
@visitor_record
def message():
    """消息列表"""
    if not sessionOperationClass.check():
        return redirect('/login/')
    # 用户名，头像, 地区
    user_name = session['login'].get('user_name', '')
    account = session['login'].get('account', '')
    avatar_url = session['login'].get('avatar_url', 'https://mp.huitouche.com/static/images/newicon.png')
    locations = [{'region_id': i, 'name': init_regions.to_full_short_name(i)} for i in
                 session['login'].get('locations', [])]
    role = session['login'].get('role', 0)
    if role == 4:
        locations = init_regions.get_city_next_region(session['login'].get('locations', []))
    return render_template('/message/message.html', user_name=user_name, avatar_url=avatar_url, locations=locations,
                           role=role, account=account)


@app.route('/edit-message/', endpoint='edit-message')
@visitor_record
def message():
    """消息管理"""
    if not sessionOperationClass.check():
        return redirect('/login/')
    # 用户名，头像, 地区
    user_name = session['login'].get('user_name', '')
    account = session['login'].get('account', '')
    avatar_url = session['login'].get('avatar_url', 'https://mp.huitouche.com/static/images/newicon.png')
    locations = [{'region_id': i, 'name': init_regions.to_full_short_name(i)} for i in
                 session['login'].get('locations', [])]
    role = session['login'].get('role', 0)
    if role == 4:
        locations = init_regions.get_city_next_region(session['login'].get('locations', []))
    return render_template('/message/edit-message.html', user_name=user_name, avatar_url=avatar_url,
                           locations=locations, role=role, account=account)

