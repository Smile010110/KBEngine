# -*- coding: utf-8 -*-

"""
通用转换函数
"""

from __future__ import annotations

import ast


def _is_empty(data) -> bool:
    return data is None or (isinstance(data, str) and len(data.strip()) == 0)


def _safe_literal_eval(data, default=None):
    if _is_empty(data):
        return default
    try:
        return ast.literal_eval(str(data))
    except Exception:
        return default


def funcPos2D(mapDict, dctData, chilidDict, data):
    """
    "x,z" -> (x, 0, z)
    """
    if _is_empty(data):
        return ()
    text = str(data)
    arr = [x.strip() for x in text.split(",")]
    if len(arr) != 2:
        return ()
    return int(arr[0]), 0, int(arr[1])


def funcInt(mapDict, dctData, chilidDict, data):
    """
    返回 int 数据
    """
    if _is_empty(data):
        return 0
    value = _safe_literal_eval(data, data)
    try:
        return int(value)
    except Exception:
        return 0


def funcFloat(mapDict, dctData, chilidDict, data):
    """
    返回 float 数据
    """
    if _is_empty(data):
        return 0.0
    try:
        return float(data)
    except Exception:
        return 0.0


def funcStr(mapDict, dctData, chilidDict, data):
    """
    返回字符串数据
    """
    if data is None:
        return ""
    return str(data)


def funcEval(mapDict, dctData, chilidDict, data):
    """
    返回 literal_eval 数据
    """
    if _is_empty(data):
        return ""
    return _safe_literal_eval(data, str(data))


def funcTupleInt(mapDict, dctData, chilidDict, data):
    """
    "1,2,3" -> (1,2,3)
    """
    if _is_empty(data):
        return ()
    text = str(data)
    return tuple(int(e.strip()) for e in text.split(",") if e.strip())


def funcTupleFloat(mapDict, dctData, chilidDict, data):
    """
    "1.1,2.2" -> (1.1,2.2)
    """
    if _is_empty(data):
        return ()
    text = str(data)
    return tuple(float(e.strip()) for e in text.split(",") if e.strip())


def funcDict(mapDict, dctData, chilidDict, data):
    """
    "1:2`3`4;2:5`6"
    -> {1: ('2','3','4'), 2: ('5','6')}
    """
    if _is_empty(data):
        return ""

    text = str(data)
    dict1 = {}
    for item in text.split(";"):
        item = item.strip()
        if not item:
            continue

        e = item.split(":", 1)
        if len(e) == 1:
            dict1[int(e[0])] = ()
        elif len(e) == 2:
            dict1[int(e[0])] = tuple(index for index in e[1].split("`") if index != "")
    return dict1


def funcTupleStr(mapDict, dctData, chilidDict, data):
    if _is_empty(data):
        return ()
    text = str(data)
    return tuple(e.strip() for e in text.split(",") if e.strip())


def funcTupleEval(mapDict, dctData, chilidDict, data):
    if _is_empty(data):
        return ()
    text = str(data)
    ret = []
    for e in text.split(","):
        e = e.strip()
        if not e:
            continue
        ret.append(_safe_literal_eval(e, e))
    return tuple(ret)


def funcTupleEvalMD(mapDict, dctData, chilidDict, data):
    """
    使用代对表转换后再 literal_eval
    """
    if _is_empty(data):
        return ()

    text = str(data)
    try:
        result = []
        for e in text.split(","):
            e = e.strip()
            if not e:
                continue
            mapped = mapDict[e]
            result.append(_safe_literal_eval(mapped, mapped))
        return tuple(result)
    except Exception as errstr:
        print(f"函数中发生错误:{errstr}")
        return ()


def funcTupleEval1(mapDict, dctData, chilidDict, data):
    """
    "1'100/2'100/3'54" -> ((1,100),(2,100),(3,54))
    """
    if _is_empty(data):
        return ()

    text = str(data)
    ret = []
    for e in text.split("/"):
        e = e.strip()
        if not e:
            continue
        try:
            i, v = e.split("'")
            ret.append((_safe_literal_eval(i, i), _safe_literal_eval(v, v)))
        except Exception as errstr:
            print(f"函数中发生错误:{errstr}")
            continue
    return tuple(ret)


def funcBool(mapDict, dctData, chilidDict, data):
    if _is_empty(data):
        return False
    try:
        return int(float(str(data))) > 0
    except Exception:
        return False


def funcNotBool(mapDict, dctData, chilidDict, data):
    return not funcBool(mapDict, dctData, chilidDict, data)


def funcNull(mapDict, dctData, chilidDict, data):
    return data


def funcZipFloat(mapDict, dctData, chilidDict, data):
    """
    float * 10000 -> int
    """
    if _is_empty(data):
        return 0
    try:
        return int(float(data) * 10000)
    except Exception:
        return 0


def funcUNZipFloat(mapDict, dctData, chilidDict, data):
    """
    int / 10000 -> float
    """
    if _is_empty(data):
        return 0.0
    try:
        return int(data) / 10000.0
    except Exception:
        return 0.0


def funcFlags(mapDict, dctData, chilidDict, data):
    """
    返回标记组合数据
    """
    if _is_empty(data):
        return 0

    val = 0
    for x in str(data).split(","):
        x = x.strip()
        if x:
            val |= int(mapDict[x])
    return val
