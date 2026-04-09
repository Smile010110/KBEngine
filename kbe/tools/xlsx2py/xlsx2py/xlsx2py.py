# -*- coding: utf-8 -*-

from __future__ import annotations

import ast
import copy
import json
import os
import re
import sys
import time
from typing import Any

import pandas as pd

from config import *
import functions
import xlsxtool
import xlsxError

try:
    import character
except Exception:
    character = functions


def hasFunc(funcName: str) -> bool:
    return hasattr(character, funcName) or hasattr(functions, funcName)


def getFunc(funcName: str):
    if hasattr(character, funcName):
        return getattr(character, funcName)
    return getattr(functions, funcName)


def is_empty(value: Any) -> bool:
    return value is None or (isinstance(value, str) and value.strip() == "")


def normalize_cell(value: Any) -> str:
    """
    统一单元格值为字符串，避免 pandas/numpy 类型干扰
    """
    if value is None:
        return ""
    if isinstance(value, float):
        if value.is_integer():
            return str(int(value))
        return str(value)
    return str(value).strip()


class Xlsx2Py:
    """
    一次读表，同时导出：
    1. 服务端 data.py
    2. 客户端 data.json（自动过滤 [S] 字段）
    """

    def __init__(self, py_outfile: str, json_outfile: str, infiles: list[str]):
        sys.excepthook = xlsxError.except_hook

        self.py_outfile = os.path.abspath(py_outfile)
        self.json_outfile = os.path.abspath(json_outfile)
        self.infiles = [os.path.abspath(p) for p in infiles]

        self.mapDict: dict[str, str] = {}
        self.headerDict: dict[str, dict[int, Any]] = {}
        self.sheet2Data: dict[str, list[tuple[str, pd.DataFrame]]] = {}
        self.all_export_sheets: list[tuple[str, str, pd.DataFrame]] = []

        self.g_dctDatas: dict[str, Any] = {}
        self.g_fdatas: dict[str, str] = {}

    # -----------------------------
    # 读取 Excel
    # -----------------------------
    def load_all_excels(self):
        self.workbooks: list[tuple[str, dict[str, pd.DataFrame]]] = []

        for infile in self.infiles:
            if not os.path.isfile(infile):
                xlsxError.error_input(EXPORT_ERROR_NOEXISTFILE, (infile,))
                continue

            print(f"开始导表:[{os.path.basename(infile)}]")

            sheets = pd.read_excel(
                infile,
                sheet_name=None,
                header=None,
                dtype=object,
                keep_default_na=False,
            )
            self.workbooks.append((infile, sheets))

    # -----------------------------
    # 构建代对表
    # -----------------------------
    def constructMapDict(self):
        for infile, sheets in self.workbooks:
            if EXPORT_MAP_SHEET not in sheets:
                continue

            df = sheets[EXPORT_MAP_SHEET]
            row_count, col_count = df.shape

            for col in range(col_count):
                for row in range(1, row_count):
                    cell = df.iat[row, col]
                    text = normalize_cell(cell)
                    if not text:
                        continue

                    text = text.replace("：", ":")
                    try:
                        k, v = text.split(":", 1)
                        self.mapDict[k.strip()] = v.strip()
                    except Exception as err:
                        print(
                            f"warning: 代对表解析失败 file={infile}, row={row + 1}, col={col + 1}, err={err}"
                        )

        if not self.mapDict:
            raise xlsxError.xe(EXPORT_ERROR_NOMAP, "无代对表或代对表为空")

    # -----------------------------
    # 收集导出表
    # -----------------------------
    def collectExportSheets(self):
        for infile, sheets in self.workbooks:
            for sheet_name, df in sheets.items():
                if not isinstance(sheet_name, str):
                    continue
                if sheet_name.startswith(EXPORT_PREFIX_CHAR):
                    pure_sheet_name = sheet_name[1:]
                    self.all_export_sheets.append((infile, pure_sheet_name, df))

        if not self.all_export_sheets:
            raise xlsxError.xe(EXPORT_ERROR_NOSHEET, "没有找到任何 @ 开头的导出表")

    # -----------------------------
    # 表头解析
    # 支持:
    #   name[!][funcInt]
    #   name[!][funcInt][S]
    # -----------------------------
    def parse_header(self, sheet_name: str, df: pd.DataFrame):
        if df.shape[0] < 1:
            raise xlsxError.xe(EXPORT_ERROR_HEADER, (sheet_name, "空表"))

        header_row = df.iloc[0].tolist()
        parsed = {}
        key_cols = []
        en_names = []

        for col_idx, raw in enumerate(header_row):
            text = normalize_cell(raw)
            if not text:
                parsed[col_idx] = None
                continue

            name, signs, funcName, server_only = self.parse_header_cell(
                text, sheet_name, col_idx + 1
            )

            converted_name = self._convert_key_name(name)

            for s in signs:
                if s not in EXPORT_ALL_SIGNS:
                    raise xlsxError.xe(
                        EXPORT_ERROR_NOSIGN, (sheet_name, 1, col_idx + 1, s)
                    )

            if EXPORT_SIGN_GTH in signs:
                key_cols.append(col_idx)

            if len(key_cols) > EXPORT_KEY_NUMS:
                raise xlsxError.xe(EXPORT_ERROR_NUMKEY, (sheet_name, 1, col_idx + 1))

            if converted_name in en_names:
                raise xlsxError.xe(
                    EXPORT_ERROR_REPEAT, (sheet_name, 1, col_idx + 1, converted_name)
                )
            en_names.append(converted_name)

            if not hasFunc(funcName):
                raise xlsxError.xe(
                    EXPORT_ERROR_NOFUNC, (sheet_name, col_idx + 1, funcName)
                )

            parsed[col_idx] = {
                "name": converted_name,
                "signs": signs,
                "func": funcName,
                "server_only": server_only,
            }

        if len(key_cols) != EXPORT_KEY_NUMS:
            raise xlsxError.xe(
                EXPORT_ERROR_NOKEY,
                (sheet_name, f"需要{EXPORT_KEY_NUMS}个主键，实际{len(key_cols)}个"),
            )

        self.headerDict[sheet_name] = parsed

    def parse_header_cell(self, text: str, sheet_name: str, col_no: int):
        """
        支持更灵活的表头：
            name[!][funcInt]
            name[!][funcInt][S]
            name[][funcStr][S]
        解析规则：
            - 第一个 '[' 之前是字段名
            - 后续 [] 块里：
                * 只包含 . $ ! 的，视为 signs
                * 等于 S 的，视为 server_only
                * 其它视为 funcName
        """
        first_bracket = text.find("[")
        if first_bracket == -1:
            raise xlsxError.xe(EXPORT_ERROR_HEADER, (sheet_name, 1, col_no, text))

        name = text[:first_bracket].strip()
        blocks = re.findall(r"\[([^\]]*)\]", text[first_bracket:])

        if not name or len(blocks) < 2:
            raise xlsxError.xe(EXPORT_ERROR_HEADER, (sheet_name, 1, col_no, text))

        signs = ""
        funcName = None
        server_only = False

        for block in blocks:
            block = block.strip()
            if block == "S":
                server_only = True
            elif all(ch in EXPORT_ALL_SIGNS for ch in block):
                signs = block
            elif funcName is None:
                funcName = block
            else:
                # 多余块直接报错，避免歧义
                raise xlsxError.xe(EXPORT_ERROR_HEADER, (sheet_name, 1, col_no, text))

        if funcName is None:
            raise xlsxError.xe(EXPORT_ERROR_HEADER, (sheet_name, 1, col_no, text))

        return name, signs, funcName, server_only

    def _convert_key_name(self, name: str):
        try:
            return ast.literal_eval(name)
        except Exception:
            return name

    # -----------------------------
    # 按 dataName 分组
    # -----------------------------
    def build_sheet2data(self):
        self.sheet2Data = {}
        for infile, pure_sheet_name, df in self.all_export_sheets:
            if pure_sheet_name not in self.mapDict:
                continue

            dataName = self.mapDict[pure_sheet_name]
            self.sheet2Data.setdefault(dataName, []).append((pure_sheet_name, df))

    # -----------------------------
    # 解析数据
    # -----------------------------
    def parse_all_data(self):
        for dataName, sheet_list in self.sheet2Data.items():
            if dataName not in self.g_dctDatas:
                self.g_dctDatas[dataName] = {}

            dctData = self.g_dctDatas[dataName]

            for pure_sheet_name, df in sheet_list:
                print(f"检测文件头: {pure_sheet_name}")
                self.parse_header(pure_sheet_name, df)

                parsed_rows = self.parse_sheet_rows(pure_sheet_name, df, dctData)
                dctData.update(parsed_rows)

            overFunc = self.mapDict.get("overFunc")
            if overFunc:
                func = getFunc(overFunc)
                dctData = func(self.mapDict, self.g_dctDatas, dctData, dataName)

            self.g_dctDatas[dataName] = dctData

        self.build_global_defs()

    def parse_sheet_rows(self, sheet_name: str, df: pd.DataFrame, dctData: dict):
        """
        第 3 行开始是数据
        Excel:
            第1行 定义
            第2行 中文
            第3行起 数据
        pandas:
            0 定义
            1 中文
            2 起 数据
        """
        result = {}
        headers = self.headerDict[sheet_name]
        tempKeys = []

        for row_idx in range(2, len(df)):
            row_series = df.iloc[row_idx]
            childDict = {}

            for col_idx in range(len(row_series)):
                header_info = headers.get(col_idx)
                if header_info is None:
                    continue

                raw_val = row_series.iloc[col_idx]
                val = normalize_cell(raw_val)

                name = header_info["name"]
                signs = header_info["signs"]
                funcName = header_info["func"]

                if "$" in signs and val:
                    if val not in self.mapDict:
                        raise xlsxError.xe(
                            EXPORT_ERROR_NOTMAP, ((row_idx + 1, col_idx + 1), val)
                        )
                    v = self.mapDict[val]
                else:
                    v = val

                if "." in signs and (v is None or str(v) == ""):
                    raise xlsxError.xe(
                        EXPORT_ERROR_NOTNULL, ((row_idx + 1, col_idx + 1), name)
                    )

                func = getFunc(funcName)
                try:
                    v = func(self.mapDict, dctData, childDict, v)
                except Exception as err:
                    raise xlsxError.xe(
                        EXPORT_ERROR_FUNC,
                        (str(err), funcName, v, row_idx + 1, col_idx + 1),
                    )

                if "!" in signs:
                    if v in tempKeys:
                        raise xlsxError.xe(
                            EXPORT_ERROR_REPKEY, ((row_idx + 1, col_idx + 1), v)
                        )
                    tempKeys.append(v)

                childDict[name] = v

            if not childDict:
                continue

            key = tempKeys[-1]
            result[key] = copy.deepcopy(childDict)
            print(f"当前:{row_idx + 1}/{len(df)}")

        return result

    # -----------------------------
    # 生成 globalDefs / allDataDefs
    # -----------------------------
    def build_global_defs(self):
        globalDefs = self.mapDict.get("globalDefs", "")
        if globalDefs:
            func = getFunc(globalDefs)
            content = func(self.g_dctDatas) if callable(func) else ""
            if content:
                self.g_fdatas["globalDefs"] = content + "\n"

        allDataDefs = self.mapDict.get("allDataDefs", "")
        if allDataDefs:
            func = getFunc(allDataDefs)
            content = func(self.g_dctDatas) if callable(func) else ""
            if content:
                self.g_fdatas["allDataDefs"] = content

    # -----------------------------
    # 导出服务端 py
    # -----------------------------
    def export_py(self):
        py_dir = os.path.dirname(self.py_outfile)
        if py_dir:
            os.makedirs(py_dir, exist_ok=True)

        print("开始写服务端 py:", self.py_outfile)
        with open(self.py_outfile, "w", encoding="utf-8") as f:
            f.write(EXPORT_DATA_HEAD)

            if "globalDefs" in self.g_fdatas:
                f.write(self.g_fdatas["globalDefs"])

            for dataName, datas in self.g_dctDatas.items():
                f.write(f"{dataName} = {repr(datas)}\n\n")

            f.write("allDatas = {\n")
            for dataName in self.g_dctDatas:
                f.write(f"    '{dataName}': {dataName},\n")

            if "allDataDefs" in self.g_fdatas:
                f.write(f"    {self.g_fdatas['allDataDefs']},\n")

            f.write("}\n")

    # -----------------------------
    # 为客户端过滤 [S] 字段
    # -----------------------------
    def build_client_data(self):
        client_all_datas = {}

        for dataName, sheet_list in self.sheet2Data.items():
            if dataName not in self.g_dctDatas:
                continue

            full_data = self.g_dctDatas[dataName]

            # 收集这个 dataName 下所有 sheet 的 server_only 字段
            server_only_fields = set()
            for pure_sheet_name, _df in sheet_list:
                headers = self.headerDict.get(pure_sheet_name, {})
                for info in headers.values():
                    if not info:
                        continue
                    if info.get("server_only"):
                        server_only_fields.add(info["name"])

            client_all_datas[dataName] = self.remove_server_fields(
                full_data, server_only_fields
            )

        return client_all_datas

    def remove_server_fields(self, data, server_only_fields: set):
        """
        递归过滤 dict 中的 [S] 字段
        只按字段名过滤，不改 list/tuple 结构
        """
        if isinstance(data, dict):
            new_data = {}
            for k, v in data.items():
                # 只过滤“字段名”
                if isinstance(k, str) and k in server_only_fields:
                    continue
                new_data[k] = self.remove_server_fields(v, server_only_fields)
            return new_data

        if isinstance(data, list):
            return [self.remove_server_fields(v, server_only_fields) for v in data]

        if isinstance(data, tuple):
            return tuple(self.remove_server_fields(v, server_only_fields) for v in data)

        return data

    # -----------------------------
    # 导出客户端 json
    # -----------------------------
    def export_json(self):
        json_dir = os.path.dirname(self.json_outfile)
        if json_dir:
            os.makedirs(json_dir, exist_ok=True)

        client_data = self.build_client_data()

        print("开始写客户端 json:", self.json_outfile)
        with open(self.json_outfile, "w", encoding="utf-8") as f:
            json.dump(
                {"allDatas": client_data},
                f,
                ensure_ascii=False,
                indent=2,
            )

    # -----------------------------
    # 主流程
    # -----------------------------
    def run(self):
        start = time.time()

        self.load_all_excels()
        self.constructMapDict()
        self.collectExportSheets()
        self.build_sheet2data()
        self.parse_all_data()
        self.export_py()
        self.export_json()

        cost = time.time() - start
        print(f"写完了，用时: {cost:.3f}s")


def main():
    """
    用法:
        python xlsx2py.py data.py data.json excel.xlsx
        python xlsx2py.py data.py data.json excel1.xlsx excel2.xlsx
    """
    if len(sys.argv) < 4:
        print(main.__doc__)
        sys.exit(1)

    py_outfile = sys.argv[1]
    json_outfile = sys.argv[2]
    infiles = sys.argv[3:]

    tool = Xlsx2Py(py_outfile, json_outfile, infiles)
    tool.run()


if __name__ == "__main__":
    main()
