# -*- encoding: utf-8 -*-
'''
init.py
----
put some words here


@Time    :   2024/04/25 17:10:24
@Author  :   Mattholy
@Version :   1.0
@Contact :   smile.used@hotmail.com
@License :   MIT License
'''

from utils.db import SessionLocal
from utils.model.orm import NodeInfo, SystemConfig
from utils.model.orm import NodeType
from env import NODE_ID, IPV6S, IPV4S

import multiprocessing
import platform
import psutil
from functools import cache
from sqlalchemy import text
from sqlalchemy.exc import OperationalError


def ready(return_stage=False) -> bool | str:
    try:
        with SessionLocal() as db:
            init_flag = db.query(SystemConfig).filter_by(
                key='init_flag').one_or_none()
            if init_flag:
                if return_stage:
                    return init_flag.value
                else:
                    return init_flag.value == 'AllDone'
            else:
                return 'NotInit' if return_stage else False
    except OperationalError as e:
        return False


def init_node(public_key: str, type: NodeType, remark: str = None, status: bool = True):
    with SessionLocal() as db:
        node: NodeInfo | None = db.query(NodeInfo).filter_by(
            node_id=NODE_ID, node_type=type).first()
        if not node:
            node = NodeInfo(
                node_id=NODE_ID,
                node_type=type,
                cpus=get_cpu_cores(),
                mem_in_gb=get_memory_gb(),
                node_name=get_hostname(),
                ipv4=','.join(IPV4S),
                ipv6=','.join(IPV6S),
                public_key=public_key,
                remark=remark
            )
            db.add(node)
        else:
            node.cpus = get_cpu_cores()
            node.mem_in_gb = get_memory_gb()
            node.node_name = get_hostname()
            node.ipv4 = ','.join(IPV4S)
            node.ipv6 = ','.join(IPV6S)
            node.remark = remark
            node.activated = status
        db.commit()


@cache
def get_cpu_cores() -> int:
    return multiprocessing.cpu_count()


@cache
def get_memory_gb() -> float:
    mem_info = psutil.virtual_memory()
    mem_total_gb = mem_info.total / 1024 / 1024 / 1024
    return mem_total_gb


@cache
def get_hostname() -> str:
    return platform.node()
