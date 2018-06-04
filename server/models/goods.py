# -*- coding: utf-8 -*-

from server import log


class GoodsList(object):

    @staticmethod
    def get_goods_list(cursor, page, limit, params):
        fileds = """shf_goods.id,
                shf_goods.NAME,
                shf_goods.weight,
                shf_goods.volume,
                
                shf_goods.type,
                shf_goods.goods_level,
                shf_goods.haul_dist,
                
                # TODO 优化
                ( SELECT shm_regions.full_short_name FROM shm_regions WHERE shf_goods.from_city_id = shm_regions.`code` ) AS from_full_name,
                ( SELECT shm_regions.short_name FROM shm_regions WHERE shf_goods.from_city_id = shm_regions.`code` ) AS from_short_name,
                ( SELECT shm_regions.full_short_name FROM shm_regions WHERE shf_goods.to_city_id = shm_regions.`code` ) AS to_full_name,
                ( SELECT shm_regions.short_name FROM shm_regions WHERE shf_goods.to_city_id = shm_regions.`code` ) AS to_short_name,
                
                shf_goods.from_address,
                shf_goods.to_address,
                
                shf_goods.mileage_total,
                shf_goods.STATUS,
                (
                SELECT
                IF
                    ( shf_goods_vehicles.attribute_value_id = 0, '不限车型', GROUP_CONCAT( shm_dictionary_items.NAME ) ) 
                FROM
                    shf_goods_vehicles
                    LEFT JOIN shm_dictionary_items ON shf_goods_vehicles.attribute_value_id = shm_dictionary_items.id 
                    AND shm_dictionary_items.is_deleted = 0 
                WHERE
                    shf_goods_vehicles.goods_id = shf_goods.id 
                    AND shf_goods_vehicles.vehicle_attribute = 1 
                    AND shf_goods_vehicles.is_deleted = 0 
                ) AS vehicle_type,
                (
                SELECT
                IF
                    ( shf_goods_vehicles.attribute_value_id = 0, '不限车长', GROUP_CONCAT( shm_dictionary_items.NAME ) ) 
                FROM
                    shf_goods_vehicles
                    LEFT JOIN shm_dictionary_items ON shf_goods_vehicles.attribute_value_id = shm_dictionary_items.id 
                    AND shm_dictionary_items.is_deleted = 0 
                WHERE
                    shf_goods_vehicles.goods_id = shf_goods.id 
                    AND shf_goods_vehicles.vehicle_attribute = 2 
                    AND shf_goods_vehicles.is_deleted = 0 
                ) AS vehicle_length,-- 新车型
                (
                SELECT
                    shf_goods_vehicles.NAME 
                FROM
                    shf_goods_vehicles 
                WHERE
                    shf_goods_vehicles.goods_id = shf_goods.id 
                    AND shf_goods_vehicles.vehicle_attribute = 3 
                    AND shf_goods_vehicles.is_deleted = 0 
                ) AS new_vehicle_type,
                (
                SELECT
                    shm_dictionary_items.NAME 
                FROM
                    shf_goods_vehicles
                    LEFT JOIN shm_dictionary_items ON shf_goods_vehicles.attribute_value_id = shm_dictionary_items.id 
                    AND shm_dictionary_items.is_deleted = 0 
                WHERE
                    shf_goods_vehicles.goods_id = shf_goods.id 
                    AND shf_goods_vehicles.vehicle_attribute = 3 
                    AND shf_goods_vehicles.is_deleted = 0 
                ) AS new_vehicle_length,
                shf_goods.price_recommend,
                shf_goods.price_expect,
                shf_goods.price_addition,
                shu_users.mobile,
                ( SELECT COUNT( * ) FROM shf_goods WHERE user_id = shu_users.id ) AS shf_goods_counts,
                (
                SELECT
                    COUNT( * ) 
                FROM
                    shu_call_records 
                WHERE
                    source_type = 1 
                    AND source_id = shf_goods.id 
                    AND ( owner_id = shf_goods.user_id OR user_id = shf_goods.user_id ) 
                ) AS call_count,
                FROM_UNIXTIME( shf_goods.create_time, '%Y-%m-%d %H:%I:%S' ) AS shf_goods_create_time,
                -- 旧版装货时间
                shf_goods.loading_time_date,
                shf_goods.loading_time_period,
                -- 新版装货时间
                shf_goods.loading_time_period_begin
        """

        command = """
                    SELECT 
                    %s
                    FROM shf_goods
                    LEFT JOIN shu_users ON shf_goods.user_id = shu_users.id
                    WHERE 1=1
                    -- 货源id
                    -- 	AND shf_goods.id = 2 and shf_goods.is_deleted = 0
                    
                    -- 货主手机
                    -- AND shu_users.mobile = 15917907641
                    
                    -- 出发地
                    -- AND (shf_goods.from_province_id = 1 OR shf_goods.from_city_id = 1 OR shf_goods.from_county_id = 440106 OR shf_goods.from_town_id = 1)
                    
                    -- 目的地
                    -- AND (shf_goods.to_province_id = 1 OR shf_goods.to_city_id = 820002 OR shf_goods.to_county_id = 1 OR shf_goods.to_town_id = 1)
                    
                    -- 货源类型
                    -- `type` tinyint(4) NOT NULL DEFAULT '1' COMMENT '货源类型：1 普通货源，2 零担货源，默认为1',
                    --  `goods_level` tinyint(4) unsigned NOT NULL DEFAULT '1' COMMENT '货源等级：1 议价货源，2 优质货源/定价货源, 3.同城定价/非优质',
                    --  `haul_dist` tinyint(4) NOT NULL DEFAULT '2' COMMENT '运输距离：1 同城，2 跨城',
                    
                    -- 同城普通货源
                    -- AND shf_goods.haul_dist = 1 AND shf_goods.type = 1
                    -- 跨城定价普通货源
                    -- AND shf_goods.haul_dist = 2 AND shf_goods.goods_level = 2 AND shf_goods.type = 1
                    -- 跨城议价普通货源
                    -- AND shf_goods.haul_dist = 2 AND shf_goods.goods_level = 1 AND shf_goods.type = 1
                    -- 零担货源
                    -- AND shf_goods.type = 2
                    
                    -- 货源状态
                        -- 下单
                        -- AND shf_goods.status = 1
                        -- 派单中
                        -- AND shf_goods.status = 2
                        -- 已生成运单
                        -- AND shf_goods.status = 3
                        -- 关闭/取消订单
                        -- AND shf_goods.status = -1
                        -- 订单时间是否过期
                        -- AND shf_goods.expired_timestamp < UNIX_TIMESTAMP()
                        
                    -- 是否通话
                    -- AND (SELECT COUNT(*)
                    -- FROM shu_call_records
                    -- WHERE source_type = 1
                    -- AND source_id = shf_goods.id
                    -- AND (owner_id = shf_goods.user_id OR user_id = shf_goods.user_id)) > 0
                    
                    -- AND (SELECT COUNT(*)
                    -- FROM shu_call_records
                    -- WHERE source_type = 1
                    -- AND source_id = shf_goods.id
                    -- AND (owner_id = shf_goods.user_id OR user_id = shf_goods.user_id)) = 0
                    
                    -- AND (SELECT COUNT(*)
                    -- FROM shu_call_records
                    -- WHERE source_type = 1
                    -- AND source_id = shf_goods.id
                    -- AND (owner_id = shf_goods.user_id OR user_id = shf_goods.user_id)) > 10
        """

        # 货源id
        if params['goods_id']:
            command += ' AND shf_goods.id = %s AND shf_goods.is_deleted = 0 ' % params['goods_id']

        # 手机
        if params['mobile']:
            command += ' AND shu_users.mobile = %s ' % params['mobile']

        # 出发地
        if params['from_region_id']:
            pass

        # 目的地
        if params['to_region_id']:
            pass

        # 货源类型
        if params['goods_type']:
            if params['goods_type'] == 1:
                command += """ AND shf_goods.haul_dist = 1 AND shf_goods.type = 1 """
            if params['goods_type'] == 2:
                command += """ AND shf_goods.haul_dist = 2 AND shf_goods.goods_level = 2 AND shf_goods.type = 1 """
            if params['goods_type'] == 3:
                command += """ AND shf_goods.haul_dist = 2 AND shf_goods.goods_level = 1 AND shf_goods.type = 1 """
            if params['goods_type'] == 4:
                command += """ AND shf_goods.type = 2 """

        # 货源状态
        if params['goods_status']:
            command += ' AND shf_goods.status = {} AND shf_goods.expired_timestamp < UNIX_TIMESTAMP() '.format(
                params['goods_status'])

        # 是否通话
        if params['is_called']:
            called_sql = """ AND (SELECT COUNT(*)
                            FROM shu_call_records
                            WHERE source_type = 1
                            AND source_id = shf_goods.id
                            AND (owner_id = shf_goods.user_id OR user_id = shf_goods.user_id)) """
            if params['is_called'] == 1:
                command += called_sql + '> 0 '
            if params['is_called'] == 2:
                command += called_sql + '= 0 '
            if params['is_called'] == 3:
                command += called_sql + '> 10 '

        # 车长要求
        if params['vehicle_length']:
            pass

        # 车型要求
        if params['vehicle_type']:
            pass

        # 所属网点
        if params['node_id']:
            pass

        # 是否初次下单
        if params['new_goods_type'] > 0:
            command += """ AND ( SELECT COUNT( * ) FROM shf_goods WHERE user_id = shu_users.id ) = 1 """

        # 急需处理
        if params['urgent_goods']:
            pass

        # 是否加价
        if params['is_addition']:
            if params['is_addition'] == 1:
                command += ' AND shf_goods.price_addition > 0 '
            elif params['is_addition'] == 2:
                command += ' AND shf_goods.price_addition = 0 '

        # 发布时间
        if params['create_start_time'] and params['create_end_time']:
            command += """ AND shf_goods.create_time > %s AND shf_goods.create_time < %s """ % (
                params['create_start_time'], params['create_end_time'])

        # 装货时间
        if params['load_start_time'] and params['load_end_time']:
            # load_start_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(params['load_start_time']))
            # load_end_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(params['load_end_time']))

            command += """ AND (( UNIX_TIMESTAMP( shf_goods.loading_time_date ) > {0} 
            AND UNIX_TIMESTAMP( shf_goods.loading_time_date ) < {1}  ) 
            OR -- 新版
            ( shf_goods.loading_time_period_begin > {0} AND shf_goods.loading_time_period_begin < {1} )) """.format(
                params['load_start_time'], params['load_end_time'])

        goods_count = cursor.query_one(command % "COUNT(*) as goods_count")['goods_count']

        command += """ LIMIT %s, %s""" % ((page - 1) * limit, limit)

        log.info('sql:{}'.format(command % fileds))
        goods_detail = cursor.query(command % fileds)

        log.info('goods_detail:{}'.format(goods_detail))

        goods_list = {'goods_detail': goods_detail if goods_detail else [],
                      'goods_count': goods_count if goods_count else 0}

        return goods_list
