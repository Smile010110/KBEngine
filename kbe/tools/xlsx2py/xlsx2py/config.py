# -*- coding: utf-8 -*-

"""
打表工具配置（Python 3 / UTF-8）
"""

###############################
# 导出 py 文件头
###############################
EXPORT_DATA_CODING = "utf-8"
EXPORT_DATA_HEAD = f"# -*- coding: {EXPORT_DATA_CODING} -*-\n\n"

###############################
# 常量
###############################
# 导出 sheet 前缀
EXPORT_PREFIX_CHAR = "@"

# 表头定义行（Excel 第 1 行）
EXPORT_DEFINE_ROW = 1

# 主键列数量
EXPORT_KEY_NUMS = 1

# 代对表相关
MAP_DEFINE_ROW = 1
MAP_DATA_ROW = 3
EXPORT_MAP_SHEET = "代对表="

# 文件编码统一 UTF-8
FILE_CODE = "utf-8"

###############################
# 命令相关
###############################
EXPORT_SIGN_DOT = "."
EXPORT_SIGN_DOLLAR = "$"
EXPORT_SIGN_GTH = "!"

CHECK_FUN = None

# format: sign: checkfunc
EXPORT_SIGN = {
    EXPORT_SIGN_DOT: CHECK_FUN,
    EXPORT_SIGN_DOLLAR: CHECK_FUN,
    EXPORT_SIGN_GTH: CHECK_FUN,
}

EXPORT_ALL_SIGNS = list(EXPORT_SIGN.keys())

###############################
# error 字典
###############################
EXPORT_ERROR_NOSHEET = 1
EXPORT_ERROR_NOMAP = 2
EXPORT_ERROR_HEADER = 3
EXPORT_ERROR_NOTNULL = 4
EXPORT_ERROR_REPEAT = 5
EXPORT_ERROR_REPKEY = 6
EXPORT_ERROR_NUMKEY = 7
EXPORT_ERROR_NOKEY = 8
EXPORT_ERROR_NOFUNC = 9

# 数据检测错误
EXPORT_ERROR_DATAINV = 20
EXPORT_ERROR_NOSIGN = 21
EXPORT_ERROR_NOTMAP = 22
EXPORT_ERROR_FUNC = 23

# 文件 IO 操作
EXPORT_ERROR_CPATH = 30
EXPORT_ERROR_FILEOPENED = 31
EXPORT_ERROR_NOEXISTFILE = 32
EXPORT_ERROR_OTHER = 101
EXPORT_ERROR_FILEOPEN = 102
EXPORT_ERROR_IOOP = 103

EXPORT_ERROR = {
    EXPORT_ERROR_NOSHEET: "无表可导",
    EXPORT_ERROR_NOMAP: "无代对表",
    EXPORT_ERROR_HEADER: "文件头错误",
    EXPORT_ERROR_NOTNULL: "不能为空",
    EXPORT_ERROR_REPEAT: "命名重复",
    EXPORT_ERROR_DATAINV: "数据与定义不符合",
    EXPORT_ERROR_OTHER: "未知错误",
    EXPORT_ERROR_NUMKEY: "需要的 key 太多",
    EXPORT_ERROR_NOSIGN: "不存在的符号",
    EXPORT_ERROR_REPKEY: "作为关键字的列有重复的 key 值",
    EXPORT_ERROR_NOTMAP: "需要代对，而没有代对关系",
    EXPORT_ERROR_NOKEY: "没有主 key",
    EXPORT_ERROR_CPATH: "目录创建失败",
    EXPORT_ERROR_FILEOPENED: "文件已打开请关闭后，再运行",
    EXPORT_ERROR_NOFUNC: "不存在的转化函数",
    EXPORT_ERROR_NOEXISTFILE: "excel 文件不存在",
    EXPORT_ERROR_FILEOPEN: "文件打开失败",
    EXPORT_ERROR_IOOP: "文件读写错误",
    EXPORT_ERROR_FUNC: "函数错误",
}

EXPORT_INFO_NULL = 0
EXPORT_INFO_OK = 1
EXPORT_INFO_ING = 2
EXPORT_INFO_CDIR = 3
EXPORT_INFO_YN = 4
EXPORT_INFO_RTEXCEL = 5

EXPORT_INFO = {
    EXPORT_INFO_NULL: "",
    EXPORT_INFO_YN: "是否继续 Y or N",
    EXPORT_INFO_OK: "文件配置正确，是否要导入(Y or N)",
    EXPORT_INFO_ING: "正在导表",
    EXPORT_INFO_CDIR: "文件已打开",
    EXPORT_INFO_RTEXCEL: "关闭文件后重试，你可以输入 O 让程序帮你关闭",
}
