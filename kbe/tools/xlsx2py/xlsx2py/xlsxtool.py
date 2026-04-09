# -*- coding: utf-8 -*-

"""
工具函数
"""

from __future__ import annotations

import os
from typing import Any

import xlsxError
from config import *


def exportMenu(msgIndex, YCallback=None, NCallback=None, OCallback=None):
    """
    原工程是命令行交互，这里保持自动继续
    """
    if YCallback:
        YCallback()
    return


def checkExtName(filePath: str, extName: str) -> bool:
    """
    检测扩展名，请把 . 也传进来
    """
    if not filePath or not extName:
        return False
    return filePath.lower().endswith(extName.lower())


def createDir(dirPath: str) -> None:
    try:
        os.makedirs(dirPath, exist_ok=True)
    except Exception:
        raise xlsxError.xe(EXPORT_ERROR_CPATH, (dirPath,))


def getFileMTime(fileName: str) -> float:
    return os.stat(fileName).st_mtime


########### 字符串处理 ####################
def inputList(var_list):
    for element in var_list:
        if isinstance(element, list):
            inputList(element)
        elif isinstance(element, str):
            inputElement(element)
        else:
            print(element)


def inputElement(element):
    if isinstance(element, str):
        print(element)
    else:
        print(element)


def str2List(error_str, pywinerr_list):
    """
    兼容旧接口，简单拆分
    """
    if not error_str:
        return
    for item in error_str.split(","):
        pywinerr_list.append(item.strip())


def val2Str(data: Any) -> str:
    if data is None:
        return ""
    if isinstance(data, float):
        if data.is_integer():
            return str(int(data))
        return str(data)
    if isinstance(data, bytes):
        return data.decode("utf-8")
    return str(data)


################################################
def list_to_text(ls):
    return repr(ls)


def tuple_to_text(t):
    return repr(t)


def dict_to_text(d):
    return repr(d)


def value_to_text(v):
    if isinstance(v, bytes):
        return repr(v.decode("utf-8"))
    return repr(v)


####################### code ############################
def toGBK(val):
    """
    为兼容旧接口保留，Python3 下不再做 gbk 转换
    """
    return val


def GTOUC(val):
    """
    旧工程里用于 gb2312 -> unicode，这里直接返回 str
    """
    if val is None:
        return ""
    if isinstance(val, bytes):
        return val.decode("utf-8")
    return str(val)


def STOU(val):
    return val


def UTOF(val):
    return val


def FTOU(val):
    return val
