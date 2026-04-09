# 源文件列表
set(SRCS
    base64.cpp
    compat.cpp
    mailer.cpp
)

# 生成静态库
add_library(jwsmtp STATIC ${SRCS})

if(NOT DEFINED KBE_ROOT)
    string(REGEX REPLACE "/kbe/src(/.*)?$" "" KBE_ROOT "${CMAKE_SOURCE_DIR}")
endif()

# 公共 include 目录
target_include_directories(jwsmtp
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR} 
)

