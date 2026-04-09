# -*- coding: utf-8 -*-

"""
错误处理
"""

from __future__ import annotations

import sys
import traceback

from config import *
import xlsxtool as xt


def except_hook(typ, val, tb):
    """
    traceback 处理
    """
    sys.__excepthook__(typ, val, tb)
    ex = "\n".join(traceback.format_exception(typ, val, tb))
    if ex:
        print(ex)
    return False


def error_input(index, args=""):
    print(f"ERROR{index}:{EXPORT_ERROR.get(index, '未知错误')}")
    if args:
        if isinstance(args, (list, tuple)):
            xt.inputList(list(args))
        else:
            print(args)
    return


def info_input(index, args=""):
    print(f"INFO({index}):{EXPORT_INFO.get(index, '')}")
    if args:
        if isinstance(args, (list, tuple)):
            xt.inputList(list(args))
        else:
            print(args)


class XlsxException(Exception):
    """
    异常处理
    """

    def __init__(self, index, msg=""):
        self.index = index
        self.msg = msg
        text = EXPORT_ERROR.get(index, "未知错误")
        super().__init__(f"ERROR{index}:{text}, {xt.value_to_text(msg)}")
        print(f"ERROR{index}:{text}, {xt.value_to_text(msg)}")
        sys.exit(1)


xe = XlsxException
