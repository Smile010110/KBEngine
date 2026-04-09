# cmakefile/Python.cmake
# 定义 KBE 自带 Python 的 INTERFACE 库

set(KBE_PYTHON_INCLUDE_DIRS
    ${KBE_ROOT}/kbe/src/lib/python/Include
    ${KBE_ROOT}/kbe/src/lib/python
    CACHE PATH "KBE Python include dirs"
)

set(KBE_PYTHON_LIB
    ${KBE_ROOT}/kbe/src/libs/libpython.a
    CACHE FILEPATH "KBE Python static library"
)

# 额外依赖
set(KBE_PYTHON_EXTRA_LIBS pthread util dl)

# 创建 INTERFACE target
add_library(KBE::Python INTERFACE IMPORTED)
set_target_properties(KBE::Python PROPERTIES
    INTERFACE_INCLUDE_DIRECTORIES "${KBE_PYTHON_INCLUDE_DIRS}"
    INTERFACE_LINK_LIBRARIES "${KBE_PYTHON_LIB};${KBE_PYTHON_EXTRA_LIBS}"
)
