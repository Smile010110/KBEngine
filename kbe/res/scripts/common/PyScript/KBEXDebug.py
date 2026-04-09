import inspect
import json
import KBEngine
import os

# 基础类型
BASIC_TYPES = (
    int,
    float,
    str,
    bool,
    type(None),
    bytes
)

BASIC_CONTAINER_TYPES = (
    list,
    tuple,
    dict,
    set,
)
BASIC_CONTAINER_TYPES_STR = (
    "list",
    "tuple",
    "dict",
    "set",
    "GlobalDataClient",
    "Entities"
)


CHILDREN_FUNC = [
    # "items",
    # "keys",
    # "values",
    # "garbages",
    "entities",
    "globalData",
    "baseAppData",
    "cellAppData",
]


def get_obj_info(obj,children_id = "",get_value = False, show_method_wrapper = False):
    try:
        attrs = {}
        childrens = {}

        for name, member in inspect.getmembers(obj):
            if name in CHILDREN_FUNC or type(member) in BASIC_CONTAINER_TYPES:
                # CHILDREN名单里的直接加入到CHILDRENS中
                childrens[f"{name}"] = {
                    "member": member,
                    "callable": callable(member),
                    "type": f"{type(member).__module__}.{type(member).__name__}",
                }

                if inspect.isfunction(member) or inspect.ismethod(member) or callable(member):
                    try:
                        sig = inspect.signature(member)
                    except ValueError:
                        sig = "(?)"
                    if name in CHILDREN_FUNC:
                        sig = "()"
                    childrens[f"{name}"]["sig"] = sig
            else:
                # 其他类型,加入到attr里
                attrs[f"{name}"] = {
                    "member": member,
                    "callable": callable(member),
                    "type": f"{type(member).__module__}.{type(member).__name__}",
                }

                if inspect.isfunction(member) or inspect.ismethod(member) or callable(member):
                    try:
                        sig = inspect.signature(member)
                    except ValueError:
                        sig = "(?)"
                    if name in CHILDREN_FUNC:
                        sig = "()"
                    attrs[f"{name}"]["sig"] = sig

        #
        # if isinstance(obj, (list, tuple)):
        #     for idx, item in enumerate(obj):
        #         childrens[idx] = {
        #             "member": item,
        #             "callable": callable(item),
        #             "type":f"{type(item).__module__}.{type(item).__name__}",
        #         }
        #
        # elif isinstance(obj, dict):
        #     for k, v in obj.items():
        #         childrens[k] = {
        #             "member": v,
        #             "callable": callable(v),
        #             "type":f"{type(v).__module__}.{type(v).__name__}",
        #         }
        #
        # elif isinstance(obj, set):
        #     for idx, item in enumerate(obj):
        #         childrens[idx] = {
        #             "member": item,
        #             "callable": callable(item),
        #             "type": f"{type(item).__module__}.{type(item).__name__}",
        #         }



        if isinstance(obj, (list, tuple)):
            for idx, item in enumerate(obj):
                childrens[idx] = {
                    "__key_type__": type(idx).__name__,
                    "member": item,
                    "callable": callable(item),
                    "type":f"{type(item).__module__}.{type(item).__name__}",
                }

        elif isinstance(obj, dict) or obj.__class__.__name__ == "GlobalDataClient" or obj.__class__.__name__ == "Entities":
            for k, v in obj.items():
                childrens[k] = {
                    "__key_type__": type(k).__name__,
                    "member": v,
                    "callable": callable(v),
                    "type":f"{type(v).__module__}.{type(v).__name__}",
                }
        elif isinstance(obj, set):
            for idx, item in enumerate(obj):
                childrens[idx] = {
                    "__key_type__": type(idx).__name__,
                    "member": item,
                    "callable": callable(item),
                    "type": f"{type(item).__module__}.{type(item).__name__}",
                }

        res = {
            "id": children_id,
            "attrs": attrs,
            "childrens": childrens,
            "type": f"{type(obj).__module__}.{type(obj).__name__}",
            "callable": callable(obj),
            "path":parse_kbe_entity_path(obj)
        }

        # if callable(obj) and type(obj()) in BASIC_CONTAINER_TYPES:
        #     res["values"] = json.dumps(obj(), ensure_ascii=False, default=str)

        KBEngine.scriptLogType(-1)
        print("--KBEX--" + json.dumps(res, ensure_ascii=False, default=str) + "--KBEX--")
    except:
        print("--KBEX--" + json.dumps({}, ensure_ascii=False, default=str) + "--KBEX--")


def parse_kbe_entity_path(obj) -> str:
    """
    根据 inspect.getfile 返回的路径，判断 entity 类型
    """
    try:
        file_path = inspect.getfile(obj.__class__)
        # 1️⃣ 内置或非法路径
        if not file_path or not isinstance(file_path, str):
            return ""

        # inspect.getfile 内置对象常见返回
        if file_path.startswith("<") and file_path.endswith(">"):
            return ""

        # 路径规范化
        path = os.path.normpath(file_path).replace("\\", "/").lower()

        # 2️⃣ base/components
        if "/base/components/" in path:
            return "base_entity_component"

        # 3️⃣ base 及其子目录
        if "/base/" in path:
            return "base_entity"

        # 4️⃣ cell/components
        if "/cell/components/" in path:
            return "cell_entity_component"

        # 5️⃣ cell 及其子目录
        if "/cell/" in path:
            return "cell_entity"
    except:
        pass
    # 其他情况
    return ""
