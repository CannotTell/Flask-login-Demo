#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/20/2017 10:50 AM
# @Author  : JZK
# @File    : adminModel.py
from flask_login import utils
import flask_admin as admin
from flask_admin import expose,AdminIndexView
from flask_admin.contrib import sqla
from db.db_Models import UserAccounts, DataLog, LoginLog


def getRequired():
    user_id = utils.session.get('user_id')
    user = UserAccounts.query.filter_by(UserName=user_id).first()
    if user.Level == 0:
        return True
    else:
        return False

class UserAccountsAdmin(sqla.ModelView):
    column_exclude_list = ['Level']
    column_searchable_list = ['UserName', 'CreateDate']
    column_filters = ['UserName', 'CreateDate']
    column_editable_list = ['Password']
    page_size = 20
    can_edit = False
    form_columns = ['UserName', 'Password', 'Remark']
    column_labels = {'UserName': u'用户名',
                     'Password': u'密码',
                     'CreateDate': u'创建日期',
                     'Remark': u'备注'}

    def is_accessible(self):
        return getRequired()


class DataLogAdmin(sqla.ModelView):
    can_create = False
    can_edit = False
    can_delete = False
    page_size = 20

    def is_accessible(self):
        return getRequired()


class LoginLogAdmin(sqla.ModelView):
    can_create = False
    can_edit = False
    can_delete = False
    page_size = 20

    column_labels = {'UserName': u'用户名',
                     'IP': u'IP地址',
                     'Address': u'IP区域',
                     'LoginDate': u'登入日期'}

    def is_accessible(self):
        return getRequired()


class MyView(AdminIndexView):
    @expose('/')
    def index(self):
        if getRequired():
            info = '欢迎使用'
        else:
            info = '您没有权限，请使用管理员账号登入'
        return self.render('admin/index.html', info = info)
