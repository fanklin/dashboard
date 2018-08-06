# -*- coding: utf-8 -*-

import time

class MessageSystemModel(object):
    @staticmethod
    def get_sys_msg_list_count(cursor):
        """查询系统消息列表总数"""
        command = """
        SELECT COUNT(*) AS count
        FROM tb_inf_system_message
        """
        result = cursor.query_one(command)
        return result['count'] if result else 0

    @staticmethod
    def get_sys_msg_list(cursor, params):
        """查询系统消息列表"""
        command = """
        SELECT id, title, content, user_id, create_time, update_time, msg_type, is_deleted
        FROM tb_inf_system_message
        ORDER BY update_time DESC
        LIMIT :page, :limit
        """
        result = cursor.query(command, params)
        return result if result else []

    @staticmethod
    def get_sys_msg_by_id(cursor, params):
        """查询系统消息"""
        command = """
        SELECT title, content, user_id, create_time, update_time, msg_type, is_deleted
        FROM tb_inf_system_message
        WHERE id = :msg_id
        """
        result = cursor.query_one(command, params)
        return result if result else {}

    @staticmethod
    def insert_system_message(cursor, params):
        """写入系统消息表"""
        command = """
        INSERT INTO tb_inf_system_message(title, content, user_id, create_time, update_time, msg_type)
        VALUES (:title, :content, :user_id, :create_time, :update_time, :msg_type)
        """
        params['create_time'] = int(time.time())
        params['update_time'] = int(time.time())
        result = cursor.insert(command, params)
        return result

    @staticmethod
    def update_system_message(cursor, params):
        """修改系统消息表"""
        command = """
        UPDATE tb_inf_system_message
        SET title = :title, content = :content, user_id = :user_id, update_time = :update_time, msg_type = :msg_type
        WHERE id = :msg_id
        """
        params['update_time'] = int(time.time())
        result = cursor.update(command, params)
        return result

    @staticmethod
    def delete_system_message(cursor, params):
        """删除系统消息表"""
        command = """
        UPDATE tb_inf_system_message
        SET is_deleted = 1
        WHERE id = :msg_id
        """
        result = cursor.update(command, params)
        return result

    @staticmethod
    def get_system_user(cursor):
        """获取后台用户"""
        command = """
        SELECT DISTINCT user_name AS account, 1 AS role
        FROM sha_users
        WHERE is_deleted = 0"""

        result = cursor.query(command)
        return result if result else []

    @staticmethod
    def get_suppliers_user(cursor):
        """获取区镇合伙人"""
        command = """
        SELECT DISTINCT shu_users.mobile AS account, 2 AS role
        FROM shd_suppliers
        INNER JOIN shu_users ON shd_suppliers.user_id = shu_users.id
        AND shu_users.is_deleted = 0
        WHERE shd_suppliers.is_deleted = 0"""

        result = cursor.query(command)
        return result if result else []

    @staticmethod
    def get_supplier_nodes(cursor):
        """获取网点管理员"""
        command = """
        SELECT DISTINCT shu_users.mobile AS account, 3 AS role
        FROM shd_supplier_nodes
        INNER JOIN shu_users ON shd_supplier_nodes.manager_user_id = shu_users.id
        AND shu_users.is_deleted = 0
        WHERE shd_supplier_nodes.is_deleted = 0"""

        result = cursor.query(command)
        return result if result else []

    @staticmethod
    def get_city_manager(cursor):
        """获取城市经理"""
        command = """
        SELECT DISTINCT account, 4 AS role
        FROM tb_inf_city_manager
        WHERE is_deleted = 0"""

        result = cursor.query(command)
        return result if result else []

    @staticmethod
    def insert_user_message(cursor, data):
        """写入用户消息表"""
        command = """
        INSERT INTO tb_inf_user_message(account, role, sys_msg_id, create_time, update_time)
        VALUES (:account, :role, :sys_msg_id, :create_time, :update_time)
        """
        result = cursor.insert(command, data)
        return result

    @staticmethod
    def delete_user_message(cursor, params):
        """删除用户消息表"""
        command = """
        UPDATE tb_inf_user_message
        SET is_deleted = 1
        WHERE sys_msg_id = :msg_id
        """
        result = cursor.update(command, params)
        return result

class MessageUserModel(object):
    @staticmethod
    def get_msg_count(cursor, params):
        """获取用户消息总数"""
        command = """
        SELECT COUNT(*) AS count
        FROM tb_inf_user_message
        WHERE account = :account
        AND is_deleted = 0
        """
        result = cursor.query_one(command, params)
        return result['count'] if result else 0

    @staticmethod
    def get_msg_unread_count(cursor, params):
        """获取用户未读消息数"""
        command = """
        SELECT COUNT(*) AS count
        FROM tb_inf_user_message
        WHERE account = :account
        AND is_deleted = 0
        AND is_read = 0
        """
        result = cursor.query_one(command, params)
        return result['count'] if result else 0

    @staticmethod
    def get_msg_data(cursor, params):
        """获取用户当前分页消息"""
        command = """
        SELECT tb_inf_user_message.id, is_read, tb_inf_user_message.create_time, tb_inf_system_message.title, tb_inf_system_message.content
        FROM tb_inf_user_message
        INNER JOIN tb_inf_system_message ON tb_inf_user_message.sys_msg_id = tb_inf_system_message.id
        WHERE account = :account
        AND tb_inf_user_message.is_deleted = 0
        ORDER BY is_read
        LIMIT :page, :limit"""

        result = cursor.query(command, params)
        return result if result else []

    @staticmethod
    def update_msg_read(cursor, params):
        """修改消息已读状态"""
        command = """
        UPDATE tb_inf_user_message
        SET is_read = 1
        WHERE account = :account AND id = :msg_id
        """

        result = cursor.update(command, params)
        return result