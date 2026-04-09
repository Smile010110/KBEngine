# 源文件列表
set(SRCS
    AABox.cpp
    Box.cpp
    Crypto.cpp
    format.cpp
    Matrix3.cpp
    Plane.cpp
    System.cpp
    Triangle.cpp
    Vector3.cpp
    Vector4.cpp
)

# 生成静态库
add_library(g3dlite STATIC ${SRCS})

# 如果没传入 KBE_ROOT，则默认取上级目录
if(NOT DEFINED KBE_ROOT)
    set(KBE_ROOT ${CMAKE_SOURCE_DIR}/../..)  # 从 g3dlite 往上三级就是根
endif()

# 公共 include 目录
target_include_directories(g3dlite
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}        # g3dlite 根目录
        ${CMAKE_CURRENT_SOURCE_DIR}/G3D    # G3D/ 目录
)
