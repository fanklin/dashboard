

class OrdersReceivedStatisticsList(object):

    @staticmethod
    def get_order_received_statistics_list(cursor, params):

        fetch_where = """ 1=1 """

        which_table = """ AND 1 """

        command = """
        SELECT
            FROM_UNIXTIME( shb_orders.create_time, '%Y-%m-%d' ) AS create_time,
            COUNT( * ) AS order_counts,
            SUM( price ) AS order_sum_price 
        FROM
            `shb_orders`
            INNER JOIN shf_goods ON shf_goods.id = shb_orders.goods_id 
            {which_table}
            WHERE
            {fetch_where}
        -- 评价 好中差
        -- and shb_orders.owner_id = shu_user_evaluations.user_id
        -- and shb_orders.driver_id = shu_user_evaluations.user_id
        
        -- AND shu_user_evaluations.`level` in (1,2)
        -- AND shu_user_evaluations.`level` = 3
        -- AND shu_user_evaluations.`level` in (4,5)
        
        -- 未支付
        -- AND shb_orders.pay_status = 1
        -- 线上支付
        -- AND shb_orders.`status` = 3 AND shb_orders.pay_status = 2 AND shf_goods.payment_method = 1
        -- 线下支付
        -- AND shb_orders.`status` = 3 AND shf_goods.payment_method = 2 AND shb_orders.paid_offline = 1
            
        GROUP BY
            FROM_UNIXTIME( shb_orders.create_time, '%Y-%m-%d' )
        """

        if params.get('start_time') and params.get('end_time'):
            fetch_where += """ AND shb_orders.create_time >= {start_time} AND
            shb_orders.create_time <= {end_time} """.format(start_time=params['start_time'], end_time=params['end_time'])

        if params.get('goods_type'):
            fetch_where += """ AND (
            ( {goods_type}=1 AND shf_goods.haul_dist = 1) OR
            ( {goods_type}=2 AND shf_goods.haul_dist = 2) OR
            ( {goods_type}=3 AND shf_goods.type = 2)
            ) """.format(goods_type=params['goods_type'])

        if params.get('comment_type'):
            which_table += """ INNER JOIN shu_user_evaluations on shb_orders.id = shu_user_evaluations.order_id """
            fetch_where += """ AND shb_orders.owner_id = shu_user_evaluations.user_id """
            fetch_where += """ 
            AND( 
                ( {comment_type}=1 AND shu_user_evaluations.`level` in (1,2)) OR
                ( {comment_type}=2 AND shu_user_evaluations.`level` = 3) OR
                ( {comment_type}=3 AND shu_user_evaluations.`level` in (4,5))
             ) """.format(comment_type=params['comment_type'])

        if params.get('pay_method'):
            fetch_where += """ 
             AND (
                ( {pay_method}=1 AND shb_orders.pay_status = 1) OR
                ( {pay_method}=2 AND shb_orders.`status` = 3 AND shb_orders.pay_status = 2 AND shf_goods.payment_method = 1) OR
                ( {pay_method}=3 AND AND shb_orders.`status` = 3 AND shf_goods.payment_method = 2 AND shb_orders.paid_offline = 1)
             )
             """.format(pay_method=params['pay_method'])

        order_received_statistics_list = cursor.query(command.format(which_table=which_table, fetch_where=fetch_where))

        data = {
            'data': order_received_statistics_list
        }

        return data
