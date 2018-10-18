import json
import time

from flask_restful import abort

from server import log
from server.cache_data import init_regions
from server.meta.decorators import make_decorator
from server.status import APIStatus, HTTPStatus, make_resp
from server.utils.date_format import get_date_aggregate


class GoodsList(object):

    @staticmethod
    @make_decorator
    def get_result(data):
        goods_detail = data['goods_detail']
        try:
            result = []
            for detail in goods_detail:

                # 构造货源状态
                goods_status = ''
                if detail.get('expire') == 1:
                    goods_status = '已过期'
                else:
                    if detail.get('STATUS') in (1, 2) and detail.get('is_deleted') == 0:
                        goods_status = '待接单'
                    elif detail.get('STATUS') == 3 and detail.get('is_deleted') == 0:
                        goods_status = '已接单'
                    elif detail.get('is_deleted') == 1:
                        goods_status = '已取消'

                # 初次下单
                mobile = detail['mobile']
                if detail['shf_goods_counts'] < 3:
                    mobile = mobile + '\n' + detail.get('user_name', '') + '\n新用户'
                else:
                    mobile = mobile + '\n' + detail.get('user_name', '') + '\n'

                # 构造运费
                price = '货主出价:%(price_expect)s元%(price_addition)s\n系统价:%(price_recommend)s元' % \
                        {
                        'price_expect': str(int(detail.get('price_expect', 0) + detail.get('price_addition', 0))),
                        'price_addition': '(+%s)' % str(int(detail['price_addition'])) if detail.get('price_addition', 0) else '',
                        'price_recommend': str(int(detail.get('price_recommend', 0)))
                        }

                # 网点
                node_id = init_regions.to_address(detail.get('from_province_id', 0), detail.get('from_city_id', 0),
                                                  detail.get('from_county_id', 0))

                # 货源价格类型
                if detail['is_system_price'] == 0:
                    goods_type = '议价'
                elif detail['is_system_price'] == 1:
                    goods_type = '一口价'
                else:
                    goods_type = ''

                # 零担需要独立判断
                if detail['type'] == 2:
                    goods_type = '零担'

                goods_type += '\n'

                # 货源距离类型
                if detail['haul_dist'] == 1:
                    goods_type += '同城'
                elif detail['haul_dist'] == 2:
                    goods_type += '跨城'
                else:
                    goods_type += '未知货源类型'

                # 构造货物规格
                goods_standard = []
                if detail['NAME']:
                    goods_standard.append(detail['NAME'])
                if detail['weight']:
                    weight = str(int(detail['weight'] * 1000)) + '千克' \
                        if detail.get('weight', 0) < 1 and detail.get('weight', 0) > 0 \
                        else str(int(detail.get('weight', 0))) + '吨'
                    goods_standard.append(weight)
                if detail['volume']:
                    volume = str(int(detail.get('volume', 0))) + 'm³'
                    goods_standard.append(volume)

                goods_standard = '\n'.join(goods_standard) if goods_standard else '没有规格'

                # 出发地-目的地
                from_address = init_regions.to_address(detail.get('from_province_id', 0), detail.get('from_city_id', 0),
                                                       detail.get('from_county_id', 0)) + detail.get('from_address',
                                                                                                     '无详细地址')
                to_address = init_regions.to_address(detail.get('to_province_id', 0), detail.get('to_city_id', 0),
                                                     detail.get('to_county_id', 0)) + detail.get('to_address', '无详细地址')
                mileage_total = str(int(detail['mileage_total'] * 1000)) + 'm' \
                    if detail.get('mileage_total', 0) < 1 and detail.get('mileage_total', 0) > 0 \
                    else str(int(detail.get('mileage_total', 0))) + 'km'

                address = '\n'.join([from_address, to_address, mileage_total])

                # 特殊车型
                extra = [
                    '需要开顶' if detail['need_open_top'] == 1 else '',
                    '需要尾板' if detail['need_tail_board'] == 1 else '',
                    '需要平板' if detail['need_flatbed'] == 1 else '',
                    '需要高栏' if detail['need_high_sided'] == 1 else '',
                    '需要箱式' if detail['need_box'] == 1 else '',
                    '需要钢板车' if detail['need_steel'] == 1 else '',
                    '需要双排座' if detail['need_double_seat'] == 1 else '',
                    '需要全拆座' if detail['need_remove_seat'] == 1 else ''
                ]
                extra = [i for i in extra if i != '']
                # 车长+特殊要求
                if detail['new_vehicle_type']:
                    L = [detail['new_vehicle_type']] + extra
                    vehicle = '\n'.join(L)
                else:
                    vehicle_type = detail['vehicle_type'] if detail['vehicle_type'] else ''
                    L = [vehicle_type] + extra
                    vehicle = '\n'.join(L)

                # 发布、装货时间
                if detail['loading_time_period_begin']:
                    loading_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(detail['loading_time_period_begin']))
                else:
                    if detail['loading_time_period'] == 1:
                        loading_time = detail.get('loading_time_date', '') + ' 08:00:00'
                    elif detail['loading_time_period'] == 2:
                        loading_time = detail.get('loading_time_date', '') + ' 13:00:00'
                    elif detail['loading_time_period'] == 3:
                        loading_time = detail.get('loading_time_date', '') + ' 19:00:00'
                    else:
                        loading_time = detail.get('loading_time_date', '') + ' 00:00:00'
                goods_time = '%(create_time)s\n%(loading_time)s' % {
                    'create_time': detail['shf_goods_create_time'],
                    'loading_time': loading_time
                }

                # 等待时间 从发布货源到被打电话的等待时间
                latency_time = '-'
                if detail.get('create_time') and detail.get('called_time'):
                    latency_time = detail.get('called_time') - detail.get('create_time')

                    latency_time = (str(int(latency_time / 3600)) + '小时' if int(
                        latency_time / 3600) > 0 else '') + \
                               (str(int(latency_time % 3600 / 60)) + '分' if int(
                                   latency_time % 3600 / 60) > 0 else '') + \
                               (str(int(latency_time % 3600 % 60)) + '秒' if int(
                                   latency_time % 3600 % 60) > 0 else '')

                result.append({
                    'id': detail['id'],
                    'mobile': mobile,
                    'shf_goods_counts': detail['shf_goods_counts'],
                    'call_count': detail['call_count'],
                    'goods_status': goods_status,
                    'price': price,
                    'node_id': node_id,
                    'goods_type': goods_type,
                    'goods_standard': goods_standard,
                    'address': address,
                    'vehicle': vehicle,
                    'goods_time': goods_time,
                    'latency_time': latency_time
                })

            result = json.loads(json.dumps(result))
            return make_resp(APIStatus.Ok, count=data['goods_count'], data=result), HTTPStatus.Ok
        except Exception as e:
            log.error('Error:{}'.format(e), exc_info=True)
            abort(HTTPStatus.BadRequest, **make_resp(HTTPStatus.BadRequest, msg='内部服务器错误'))


class GoodsDistributionTrend(object):

    @staticmethod
    @make_decorator
    def get_result(data, params):
        all_order = data['all_order']
        wait_order = data['wait_order']
        recv_order = data['recv_order']
        cancel_order = data['cancel_order']

        xAxis, goods_user_count_series = get_date_aggregate(params["start_time"], params["end_time"], params["periods"], all_order, number_field='goods_user_count')
        _, wait_order_series = get_date_aggregate(params["start_time"], params["end_time"], params["periods"], wait_order)
        _, recv_order_series = get_date_aggregate(params["start_time"], params["end_time"], params["periods"], recv_order)
        _, cancel_order_series = get_date_aggregate(params["start_time"], params["end_time"], params["periods"], cancel_order)

        ret = {
            'xAxis': xAxis,
            'wait_order_series': wait_order_series,
            'recv_order_series': recv_order_series,
            'cancel_order_series': cancel_order_series,
            'goods_user_count_series': goods_user_count_series
        }
        return make_resp(APIStatus.Ok, data=ret), HTTPStatus.Ok
