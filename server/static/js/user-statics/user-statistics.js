$('#date_show_one').val(String(common.getNowFormatDate()[2]));
$('#date_show_two').val(String(common.getNowFormatDate()[3]));
var requestStart = $('#date_show_one').val() + ' 00:00:00';
var requestEnd = $('#date_show_two').val() + ' 23:59:59';
setTimeout(function () {
    common.dateInterval($('#date_show_one').val(), $('#date_show_one').val());
}, 100);
$('#area_select').address({
    offsetLeft: '0',
    level: 3,
    onClose: function () {
    }
});
layui.use(['laydate', 'layer', 'form', 'table'], function () {
    dataInit();
    var laydate = layui.laydate;
    var table = layui.table;
    var layer = layui.layer;
    layer.load();
    laydate.render({
        elem: '#date_show_one',
        theme: '#009688',
        calendar: true,
        max: String(common.getNowFormatDate()[3]),
        ready: function () {

        },
        done: function (val, index) {
            var startTime = $('#date_show_one').val();
            var endTime = $('#date_show_two').val();
            common.dateInterval(endTime, startTime);
            if (common.timeTransform(startTime) > common.timeTransform(endTime)) {
                layer.msg('提示：开始时间大于了结束时间！');
                return false
            }
        }
    });
    laydate.render({
        elem: '#date_show_two',
        theme: '#009688',
        calendar: true,
        max: String(common.getNowFormatDate()[3]),
        ready: function () {
            if ($('#date_show_three').val() == '') {
                $('#date_show_three').next('.date-tips').show();
            } else {
                $('#date_show_three').next('.date-tips').hide()
            }
        },
        done: function (val, index) {
            var startTime = $('#date_show_one').val();
            var endTime = $('#date_show_two').val();
            common.dateInterval(endTime, startTime);
            if (common.timeTransform(startTime) > common.timeTransform(endTime)) {
                layer.msg('提示：开始时间大于了结束时间！');
                return false
            }
        }
    });
    laydate.render({
        elem: '#date_show_three',
        theme: '#009688',
        calendar: true,
        max: String(common.getNowFormatDate()[3]),
        ready: function () {
            if ($('#date_show_three').val() == '') {
                $('#date_show_three').next('.date-tips').show();
            } else {
                $('#date_show_three').next('.date-tips').hide()
            }
        },
        done: function (val, index) {
            if ($('#date_show_three').val() == '') {
                $('#date_show_three').next('.date-tips').show();
            } else {
                $('#date_show_three').next('.date-tips').hide()
            }
            var startTime = common.timeTransform($('#date_show_three').val())
            var endTime = common.timeTransform($('#date_show_four').val())
            if (startTime > endTime) {
                layer.msg('提示：开始时间大于了结束时间！');
                return false;
            }
        }
    });
    laydate.render({
        elem: '#date_show_four',
        theme: '#009688',
        calendar: true,
        max: String(common.getNowFormatDate()[3]),
        ready: function () {
            if ($('#date_show_four').val() == '') {
                $('#date_show_four').next('.date-tips').show();
            } else {
                $('#date_show_four').next('.date-tips').hide()
            }
        },
        done: function (val, index) {
            if ($('#date_show_three').val() == '') {
                $('#date_show_three').next('.date-tips').show();
            } else {
                $('#date_show_three').next('.date-tips').hide()
            }
            var startTime = common.timeTransform($('#date_show_three').val())
            var endTime = common.timeTransform($('#date_show_four').val())
            if (startTime > endTime) {
                layer.msg('提示：开始时间大于了结束时间！');
                return false;
            }
        }
    });
    laydate.render({
        elem: '#date_show_five',
        theme: '#009688',
        max: String(common.getNowFormatDate()[3]),
        calendar: true,
        ready: function () {

        },
        done: function (val, index) {
            if ($('#date_show_five').val() == '') {
                $('#date_show_five').next('.date-tips').show();
            } else {
                $('#date_show_five').next('.date-tips').hide()
            }
            var startTime = common.timeTransform($('#date_show_five').val())
            var endTime = common.timeTransform($('#date_show_six').val())
            if (startTime > endTime) {
                layer.msg('提示：开始时间大于了结束时间！');
                return false;
            }
        }
    });
    laydate.render({
        elem: '#date_show_six',
        theme: '#009688',
        max: String(common.getNowFormatDate()[3]),
        calendar: true,
        ready: function () {

        },
        done: function (val, index) {
            if ($('#date_show_six').val() == '') {
                $('#date_show_six').next('.date-tips').show();
            } else {
                $('#date_show_six').next('.date-tips').hide()
            }
            var startTime = common.timeTransform($('#date_show_five').val())
            var endTime = common.timeTransform($('#date_show_six').val())
            if (startTime > endTime) {
                layer.msg('提示：开始时间大于了结束时间！');
                return false;
            }
        }
    });
    table.render({
        elem: '#LAY_table_user'
        , url: '/user/list/',
        even: true,
        response: {
            statusName: 'status',
            statusCode: 100000
        },
        done: function (res, curr, count) {
            $('[data-field]>div').css({'padding': '0 6px'})
            $("[data-field='user_type']").children().each(function () {
                if ($(this).text() == 0) {
                    $(this).text('未录入')
                } else if ($(this).text() == 1) {
                    $(this).text('货主')
                } else if ($(this).text() == 2) {
                    $(this).text('司机')
                } else if ($(this).text() == 3) {
                    $(this).text('物流公司')
                }
            })

            $("td[data-field='goods_count']").children().each(function () {
                if ($(this).text() != '') {
                    var str = $(this).text();
                    $(this).html(str + '次')
                }
            })
            $("td[data-field='order_count']").children().each(function () {
                if ($(this).text() != '') {
                    var str = $(this).text();
                    $(this).html(str + '次')
                }
            })
            $("td[data-field='mobile']").children().each(function () {
                if ($(this).text().length > 12) {
                    var result = $(this).text().split('\n');
                    console.log(result)
                    $(this).html('<span>' + result[0] + '</span ><br><span style="color: #f40;">(' + result[1] + ')</span>')
                }
            })
            $("td[data-field='order_completed']").children().each(function () {
                if ($(this).text() != '') {
                    var str = $(this).text();
                    $(this).html(str + '单')
                }
            })
        }
        , cols: [[
            {field: 'id', title: '用户ID', sort: true, width: 86},
            {field: 'user_name', title: '用户名', width: 106}
            , {field: 'mobile', title: '手机号', width: 111}
            , {field: 'user_type', title: '注册角色', width: 111}
            , {field: 'role_auth', title: '认证', width: 111}
            , {field: 'goods_count', title: '发货', width: 80}
            , {field: 'order_count', title: '接单', width: 76}
            , {field: 'order_completed', title: '完成订单', width: 76}
            , {field: 'download_channel', title: '下载渠道', width: 110}
            , {field: 'from_channel', title: '注册渠道', width: 146}
            , {field: 'last_login_time', title: '最后登陆', width: 104}
            , {field: 'create_time', title: '注册时间', width: 104}
            , {field: 'usual_city', title: '常驻地'}
        ]]

        , id: 'testReload'
        , page: true
    });
    var $ = layui.$, active = {
        reload: function () {
            var demoReload = $('#demoReload');
            table.reload('testReload', {
                page: {
                    curr: 1
                }
                , where: {
                    key: {
                        id: demoReload.val()
                    }
                }
            });
        }
    };
    $('.dataTable .layui-btn').on('click', function () {
        var type = $(this).data('type');
        active[type] ? active[type].call(this) : '';
    });
});
$('#user_search_box').on('click', function (e) {
    e.preventDefault();
    var beginTime = $.trim($('#date_show_three').val()+' 00:00:00');
    var finishTime = $.trim($('#date_show_four').val()+' 23:59:59');
    var infinteTime = $.trim($('#date_show_five').val()+' 00:00:00');
    var overTIme = $.trim($('#date_show_six').val()+' 23:59:59');
    var provinceid = $.trim($('#area_select').attr('provinceid'));
    var cityid = $.trim($('#area_select').attr('cityid'));
    var districtsid = $.trim($('#area_select').attr('districtsid'));
    if ($('#phone_number').val() != '' && $('#phone_number').val().length != 11) {
        layer.msg('请检查用户名号码长度!', function () {

        });
        return false;
    }
    if ($('#reference_mobile').val() != '' && $('#reference_mobile').val().length != 11) {
        layer.msg('请检查推荐人号码长度!', function () {

        });
        return false;
    }

    if (beginTime !== '' && finishTime == '') {
        layer.msg('请选择最后登陆的结束日期', function () {

        });
        return false;
    }
    if (beginTime == '' && finishTime != '') {
        layer.msg('请选择最后登陆的起始日期', function () {

        });
        return false;
    }
    if (beginTime != '') {
        beginTime = common.timeTransform(beginTime)
    }
    if (finishTime != '') {
        finishTime = common.timeTransform(finishTime)
    }
    if (infinteTime != '') {
        infinteTime = common.timeTransform(infinteTime)
    }
    if (overTIme != '') {
        overTIme = common.timeTransform(overTIme)
    }
    if (infinteTime !== '' && overTIme == '') {
        layer.msg('请选择注册日期的结束日期', function () {

        });
        return false
    }
    if (infinteTime == '' && overTIme != '') {
        layer.msg('请选择注册日期的开始日期', function () {

        });
        return false;
    }

    var data = {
        user_name: $.trim($('#user_name').val()),
        mobile: $.trim($('#phone_number').val()),
        reference_mobile: $.trim($('#reference_mobile').val()),
        download_ch: $.trim($('#download_ch').val()),
        from_channel: $.trim($('#register').val()),
        is_referenced: $.trim($('#is_referenced').val()),
        home_station_province: provinceid,
        home_station_city: cityid,
        home_station_county: districtsid,
        role_type: $.trim($('#role_type').val()),
        role_auth: $.trim($('#role_auth').val()),
        is_actived: $.trim($('#is_actived').val()),
        is_used: $.trim($('#is_used').val()),
        is_car_sticker: $.trim($('#is_car_sticker').val()),
        last_login_start_time: beginTime,
        last_login_end_time: finishTime,
        register_start_time: infinteTime,
        register_end_time: overTIme,
        page: 1,
        limit: 10
    }
    var url = '/user/list/?user_name=' + data.user_name + '&mobile=' + data.mobile + '&reference_mobile=' + data.reference_mobile + '&download_ch=' + data.download_ch + '&from_channel=' +
        data.from_channel + '&is_referenced=' + data.is_referenced + '&home_station_province=' + data.home_station_province + '&home_station_city=' + data.home_station_city + '&home_station_county=' + data.home_station_county + '&role_type=' + data.role_type + '&role_auth=' + data.role_auth + '&is_actived=' + data.is_actived + '&is_used=' + data.is_used + '&is_car_sticker=' + data.is_car_sticker + '&last_login_start_time=' + data.last_login_start_time + '&last_login_end_time=' + data.last_login_end_time + '&register_start_time=' + data.register_start_time + '&register_end_time=' + data.register_end_time;

    layui.use('table', function () {
        var table = layui.table;
        table.render({
            url: url
            , elem: '#LAY_table_user'
            , even: true
            , response: {
                statusName: 'status',
                statusCode: 100000
            }
            , done: function () {
                $('[data-field]>div').css({'padding': '0 6px'})
                $("[data-field='user_type']").children().each(function () {
                    if ($(this).text() == 0) {
                        $(this).text('未录入')
                    } else if ($(this).text() == 1) {
                        $(this).text('货主')
                    } else if ($(this).text() == 2) {
                        $(this).text('司机')
                    } else if ($(this).text() == 3) {
                        $(this).text('物流公司')
                    }
                })

                $("td[data-field='goods_count']").children().each(function () {
                    if ($(this).text() != '') {
                        var str = $(this).text();
                        $(this).html(str + '次')
                    }
                })
                $("td[data-field='order_count']").children().each(function () {
                    if ($(this).text() != '') {
                        var str = $(this).text();
                        $(this).html(str + '次')
                    }
                })
                $("td[data-field='order_completed']").children().each(function () {
                    if ($(this).text() != '') {
                        var str = $(this).text();
                        $(this).html(str + '单')
                    }
                })
            }
            , cols: [[
                {field: 'id', title: '用户ID', sort: true, width: 86},
                {field: 'user_name', title: '用户名', width: 106}
                , {field: 'mobile', title: '手机号', width: 111}
                , {field: 'user_type', title: '注册角色', width: 111}
                , {field: 'role_auth', title: '认证', width: 111}
                , {field: 'goods_count', title: '发货', width: 80}
                , {field: 'order_count', title: '接单', width: 76}
                , {field: 'order_completed', title: '完成订单', width: 76}
                , {field: 'download_channel', title: '下载渠道', width: 110}
                , {field: 'from_channel', title: '注册渠道', width: 146}
                , {field: 'last_login_time', title: '最后登陆', width: 104}
                , {field: 'create_time', title: '注册时间', width: 104}
                , {field: 'usual_city', title: '常驻地'}
            ]]
            , id: 'testReload'
            , page: true
        });
    })
});
$('#search_btn').on('click', function (e) {
    e.preventDefault();
    dataInit()
})
$(window).load(function () {
    layer.closeAll('loading')
})

function dataInit() {
    var requestStartTime = common.timeTransform($('#date_show_one').val() + ' 00:00:00');
    var requestEndTime = common.timeTransform($('#date_show_two').val() + ' 23:59:59');
    var data = {
        start_time: requestStartTime,
        end_time: requestEndTime,
        periods: $('.periods>li').find('button.active').val(),
        user_type: $('#user_type').val(),
        role_type: $('#role_type_first').val(),
        region_id: $('#region_id').val(),
        is_auth: $("#is_auth").val()
    };
    var url = '/user/statistic/'
    http.ajax.get_no_loading(true, false, url, data, http.ajax.CONTENT_TYPE_2, function (res) {
        if (res.status == 100000) {
            var len = res.data.xAxis.length;
            var X_data = res.data.xAxis;
            if (len > 0 && len < 20) {
                $('.chart-tips').css({'display': 'none'})
                chartInit(res.data.xAxis, res.data.series, 1, X_data[1])
            } else if (len > 0 && len > 20 && len < 40) {
                $('.chart-tips').css({'display': 'none'})
                chartInit(res.data.xAxis, res.data.series, 2, X_data[1])
            } else if (len > 0 && len > 40 && len < 90) {
                $('.chart-tips').css({'display': 'none'})
                chartInit(res.data.xAxis, res.data.series, 4, X_data[1])
            }
        }
    })
}

Highcharts.setOptions({
    colors: ['#37A2DA', '#32C5E9', '#67E0E3', '#9FE6B8', '#FFDB5C', '#ff9f7f', '#fb7293', '#E062AE', '#E690D1', '#e7bcf3', '#9d96f5', '#8378EA', '#96BFFF']
});

function chartInit(xAxis, series, interval, x_value1) {
    $('#charts_container_one').highcharts({
        tooltip: {
            shared: true,
            crosshairs: [{
                width: 1,
                color: '#ccc'
            }, {
                width: 1,
                color: '#ccc'
            }]
        },
        chart: {
            zoomType: 'xy'
        },

        title: {
            text: '用户变化趋势曲线图'
        },
        subtitle: {
            text: null
        },
        legend: {
            layout: 'vertical',
            align: 'left',
            verticalAlign: 'top',
            x: 1000,
            y: 0,
            floating: true,
            borderWidth: 1,
            backgroundColor: 'transparent',
            labelFormatter: function () {
                return this.name
            }
        },
        xAxis: {
            tickInterval: interval,
            categories: xAxis,
            gridLineColor: '#eee',
            gridLineWidth: 1
        },
        yAxis: {
            gridLineColor: '#eee',
            gridLineWidth: 1,
            plotLines: [
                {
                    color: '#ddd',
                    dashStyle: 'dash',
                    value: x_value1,
                    width: 1
                }
            ],
            title: {
                text: '人数 (人)',
                style: {
                    color: Highcharts.getOptions().colors[0]
                }
            },
            labels: {
                format: '{value} 人',
                style: {
                    color: Highcharts.getOptions().colors[0]
                }
            }
        },
        plotOptions: {
            line: {
                dataLabels: {
                    enabled: true
                }
            },
            series: {
                states: {
                    hover: {
                        enabled: true
                    }
                }
            }
            , marker: {
                radius: 3.5,
                lineWidth: 1,
                //  lineColor: '#666666',
                symbol: 'circle',

                states: {
                    hover: {
                        enabled: true,
                        radius: 3.5
                    }
                }
            },
        },
        series: [{
            name: '人数',
            type: 'line',
            tooltip: {
                valueSuffix: '人'
            },
            data: series
        }]
    });
}
