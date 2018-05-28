# coding=utf-8
# author=veficos
from functools import wraps

from server import log


class MouldingError(Exception):
    pass


class MetaModel(type):

    def _handler(cls, e, *args, **kwargs):
        raise e

    def __new__(cls, name, bases, tpls):
        table = tpls.get('table', '')
        table_fields = tpls.get('table_fields', set())
        handler = tpls.get('handler', cls._handler)
        description = tpls.get('description', '')

        def collect_exception():
            def decorator(real_func):
                @wraps(real_func)
                def wrapper(*real_args, **real_kwargs):
                    try:
                        if len(real_kwargs) == 1 and 'where_list' in real_kwargs.keys():
                            # 外部拼接的 where 直接传入
                            last_result = real_func(*real_args, where_list=real_kwargs['where_list'], kwargs={})
                        else:
                            # 转换 where 语句
                            where_list = []
                            log.info('real_kwargs:{}'.format(real_kwargs))
                            for k in real_kwargs.keys():
                                if isinstance(real_kwargs[k], list) and str(real_kwargs[k][0]).isdigit():
                                    where_list.append('`%s` IN (%s)' % (k, ','.join([str(x) for x in real_kwargs[k]])))
                                elif isinstance(real_kwargs[k], list) and not str(real_kwargs[k][0]).isdigit():
                                    where_list.append('`%s` IN (%s)' %
                                                      (k, ','.join(['"%s"' % str(x) for x in real_kwargs[k]])))
                                else:
                                    where_list.append('`%s`=:%s' % (k, k))

                            # where_list = ['`is_deleted`=:is_deleted', '`device_type` IN (1,2)', '`user_id`=:user_id']
                            log.info('where_list:{}'.format(where_list))
                            last_result = real_func(*real_args, where_list=where_list, kwargs=real_kwargs)
                        return last_result
                    except Exception as e:
                        return handler(cls, e, description, real_func.__doc__, *real_args, **real_kwargs)

                return wrapper

            return decorator

        def fetch_fields(cursor):
            # 获取表全部字段
            try:
                command = 'SHOW FULL FIELDS  FROM {table}'.format(table=table)
                result = cursor.query(command)
                table_fields.update(set([x['Field'] for x in result]))
            except Exception as e:
                raise MouldingError('moulding %s failure: %s' % (table, str(e)))

        @collect_exception()
        def query_one(cursor, where_list, kwargs):
            """获取一个"""
            command = 'SELECT * FROM %s' % table
            if where_list:
                command += ' WHERE ' + ' AND '.join(where_list)
            # command = 'select * from shu_refreshtokens
            # WHERE `is_deleted`=:is_deleted
            # AND `device_type` IN (1,2)
            # AND `user_id`=:user_id'
            print(command)
            log.info('SqlKwargs:{}'.format(kwargs))
            result = cursor.query_one(command, kwargs)
            return result if result else {}

        @collect_exception()
        def query(cursor, where_list, kwargs):
            """获取列表"""
            command = 'SELECT * FROM %s' % table
            if where_list:
                command += ' WHERE ' + ' AND '.join(where_list)
            print(command)
            log.info('SqlKwargs:{}'.format(kwargs))
            result = cursor.query(command, kwargs)
            return result if result else []

        @collect_exception()
        def query_exists(cursor, where_list, kwargs):
            """是否存在"""
            command = 'SELECT * FROM %s' % table
            if where_list:
                command += ' WHERE ' + ' AND '.join(where_list)
            command = "SELECT exists(%s) AS exist" % command
            print(command)
            log.info('SqlKwargs:{}'.format(kwargs))
            result = cursor.query(command, kwargs)
            return result[0]['exist'] if result else 0

        @collect_exception()
        def query_count(cursor, where_list, kwargs):
            """统计数量"""
            command = 'SELECT COUNT(1) as count FROM %s' % table
            if where_list:
                command += ' WHERE ' + ' AND '.join(where_list)
            print(command)
            result = cursor.query(command, kwargs)
            return result[0]['count'] if result else 0

        @collect_exception()
        def query_paging(cursor, index, count, order_by, where_list, kwargs):
            """分页列表"""
            command = 'SELECT * FROM %s' % table
            if where_list:
                command += ' WHERE ' + ' AND '.join(where_list)
            command += ' order by %s limit %s, %s' % (order_by, (index - 1) * count, count)
            print(command)
            result = cursor.query(command, kwargs)
            return result if result else []

        @collect_exception()
        def delete(cursor, where_list, kwargs):
            """删除"""
            command = 'DELETE FROM %s' % table
            if not where_list:
                # 禁止全表删除
                raise MouldingError('delete full table error')
            command += ' WHERE ' + ' AND '.join(where_list)
            print(command)
            return cursor.delete(command, kwargs)

        @collect_exception()
        def update(cursor, fields, where_list, kwargs):
            """更新"""
            if not fields or not where_list:
                # 禁止全表更新
                raise MouldingError("Unknown field or no where_list")

            if not table_fields:
                fetch_fields(cursor)

            if set(fields) - set(table_fields):
                raise MouldingError('Unknown field %s' % (set(fields) - set(table_fields)))

            command = 'UPDATE %s set %s ' % (table, ','.join([''.join(['`%s`="%s"' % (v, fields[v])]) for v in fields]))

            command += ' WHERE ' + ' AND '.join(where_list)
            print(command)
            return cursor.update(command, kwargs)

        def insert(cursor, values):
            """新增"""
            if not values:
                return 0

            if not table_fields:
                fetch_fields(cursor)

            if isinstance(values, list) and isinstance(values[0], dict):
                fields = table_fields & set(values[0].keys()) - {'id'}
            elif isinstance(values, dict):
                fields = table_fields & set(values.keys()) - {'id'}
            else:
                raise MouldingError('values type error')

            command = '''INSERT INTO {table} ({fields}) VALUES ({values})'''\
                .format(table=table,
                        fields=','.join(['`%s`' % v for v in fields]),
                        values=','.join([':%s' % v for v in fields]))
            print(command)
            return cursor.insert(command, values)

        tpls['query_one'] = staticmethod(query_one)
        tpls['query'] = staticmethod(query)
        tpls['query_count'] = staticmethod(query_count)
        tpls['query_exists'] = staticmethod(query_exists)
        tpls['query_paging'] = staticmethod(query_paging)
        tpls['delete'] = staticmethod(delete)
        tpls['update'] = staticmethod(update)
        tpls['insert'] = staticmethod(insert)
        return super().__new__(cls, name, bases, tpls)


if __name__ == '__main__':

    import db


    class BaseModel(metaclass=MetaModel):
        pass


    class ReadORMModel(object):

        @staticmethod
        def query_one(cursor, **payload):
            return {}

        @staticmethod
        def query_count(cursor, **payload):
            return 1

        @staticmethod
        def query_exists(cursor, **payload):
            return True

        @staticmethod
        def query(cursor, **payload):
            return []

        @staticmethod
        def query_paging(cursor, index, count, order_by, **payload):
            return []


    class WriteORMModel(object):

        @staticmethod
        def delete(cursor, **payload):
            return 1

        @staticmethod
        def update(cursor, fields, **payload):
            return 1

        @staticmethod
        def insert(cursor, payload):
            return 1


    class LockModel(BaseModel, ReadORMModel, WriteORMModel):
        table = 'shx_locks'
        description = "锁"

        def handler(self, e, description, doc, *args, **kwargs):
            print([description, doc, args, kwargs])
            raise e

    reader = db.MySQLdb({
        "maxConnections": 3,
        "port": 3306,
        "host": "huitouche2.mysql.rds.aliyuncs.com",
        "minFreeConnections": 1,
        "database": "sshuitouche",
        "password": "htctita337",
        "user": "sshtc_user",
        "charset": "utf8mb4",
        "keepConnectionAlive": True
    })

    LockModel.delete(reader, where_list=["1=1"])

    the_id = LockModel.insert(reader, [
        {
            'type': 0,
            'lock_code': 'vvv',
            'create_time': 0,
        }
    ])
    assert isinstance(the_id, int)
    print("insert %s" % the_id)
    print(LockModel.query_one(reader, where_list=["id=%s" % the_id]))

    lock = LockModel.query_one(reader, id=the_id)
    assert isinstance(lock, dict) and lock != {}
    print("query_one id %s" % lock)

    no_lock = LockModel.query_one(reader, id=the_id + 1)
    assert isinstance(no_lock, dict) and no_lock == {}
    print("query_one id+1 get None %s" % no_lock)

    lock_list = LockModel.query(reader, **{
        "type": 0
    })
    assert isinstance(lock_list, list) and lock_list != []
    print("query {'type': 0} %s" % lock_list)

    lock_list = LockModel.query(reader, **{
        "lock_code": 'vvv'
    })
    assert isinstance(lock_list, list) and lock_list != []
    print("query {'type': 0} %s" % lock_list)

    lock_list = LockModel.query(reader, lock_code=['vvv', 'asdas'])
    assert isinstance(lock_list, list) and lock_list != []
    print("query lock_code=['vvv'] %s" % lock_list)

    lock_list = LockModel.query(reader, id=[the_id, the_id+1])
    assert isinstance(lock_list, list) and lock_list != []
    print("query id=[the_id] %s" % lock_list)

    lock_list = LockModel.query(reader, **{
        "type": 1
    })
    assert isinstance(lock_list, list) and lock_list == []
    print("query {'type': 1} None %s" % lock_list)

    try:
        LockModel.update(reader, {'type': 1}, **{})
    except MouldingError as e:
        print("\n    update full table error\n")
    except BaseException as e:
        raise e

    update_lock = LockModel.update(reader, {'type': 1}, id=[the_id])
    assert isinstance(update_lock, int) and update_lock == 1
    print("update %s" % update_lock)

    update_lock = LockModel.update(reader, {'type': 1}, id=[the_id])
    assert isinstance(update_lock, int) and update_lock == 0
    print("update None %s" % update_lock)

    lock_list = LockModel.query_paging(reader, 1, 10, 'id desc', **{})
    assert isinstance(lock_list, list) and len(lock_list) == 1 and lock_list[0]["type"] == '1'
    print("query_paging 1, 10, 'id desc' %s" % lock_list)

    try:
        LockModel.delete(reader, **{})
    except MouldingError as e:
        print("\n    delete full table error\n")
    except BaseException as e:
        raise e

    delete_lock = LockModel.delete(reader, id=the_id)
    assert isinstance(delete_lock, int) and delete_lock == 1
    print("delete id %s" % delete_lock)

    lock_list = LockModel.query_paging(reader, 1, 10, 'id desc', **{})
    assert isinstance(lock_list, list) and lock_list == []
    print("query_paging 1, 10, 'id desc' None %s" % lock_list)
