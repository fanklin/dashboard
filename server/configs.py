# -*- coding: utf-8 -*-

from server.superconf import SuperConf
from server.superconf.jsonserialize import JsonSerialize
from server.superconf.kazooengine import KazooEngine
from server.superconf.engine import Engine

import os

# 读取zookeeper中配置文件
configs = SuperConf(serialize=JsonSerialize(remote_filename=''.join([str(os.getpid()), '-', 'superconf.json'])),
                    engine=KazooEngine(
                        hosts=SuperConf(JsonSerialize(), engine=Engine()).env.zookeeper.host
                        ), root='superconf')

@configs.register('.bi_dashboard.mysql.read_prod')
def __read_prod(conf):
    pass


@configs.register('.bi_dashboard.mysql.read_bi')
def __read_bi(conf):
    pass


@configs.register('.bi_dashboard.mysql.write_bi')
def __write_bi(conf):
    pass


@configs.register('.bi_dashboard.log')
def __log(conf):
    pass
