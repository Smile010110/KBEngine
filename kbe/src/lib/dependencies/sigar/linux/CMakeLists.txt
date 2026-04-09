project(sigar C) 
# 源文件列表
set(SRCS
	sigar.c
	sigar_cache.c
	sigar_fileinfo.c
	sigar_format.c
	sigar_getline.c
	sigar_ptql.c
	sigar_signal.c
	sigar_util.c
	linux_sigar.c
)

# find_path(TIRPC_INCLUDE_DIR rpc/rpc.h)
# if(TIRPC_INCLUDE_DIR)
#     target_include_directories(sigar PUBLIC ${TIRPC_INCLUDE_DIR})
# endif()


# if(UNIX AND NOT APPLE)
#     find_path(TIRPC_INCLUDE_DIR NAMES rpc/rpc.h PATHS /usr/include/tirpc)
#     find_library(TIRPC_LIB NAMES tirpc PATHS /usr/lib /usr/lib/x86_64-linux-gnu)

#     if(TIRPC_INCLUDE_DIR AND TIRPC_LIB)
#         message(STATUS "Found libtirpc: ${TIRPC_LIB}, include: ${TIRPC_INCLUDE_DIR}")
#         target_include_directories(sigar PUBLIC ${TIRPC_INCLUDE_DIR})
#         target_link_libraries(sigar PUBLIC ${TIRPC_LIB})
#     else()
#         message(FATAL_ERROR "libtirpc not found. Did you install libtirpc-dev?")
#     endif()
# endif()

# 生成静态库
add_library(sigar STATIC ${SRCS})

# 如果没传入 KBE_ROOT，则默认取上级目录
if(NOT DEFINED KBE_ROOT)
    set(KBE_ROOT ${CMAKE_SOURCE_DIR}/../../..) 
endif()




# 包含头文件
target_include_directories(sigar PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})


find_package(PkgConfig REQUIRED)
pkg_check_modules(TIRPC REQUIRED libtirpc)

if(TIRPC_FOUND)
    target_include_directories(sigar PUBLIC ${TIRPC_INCLUDE_DIRS})
    target_link_libraries(sigar PUBLIC ${TIRPC_LIBRARIES})
else()
    message(FATAL_ERROR "libtirpc not found. Please install libtirpc-dev (Debian/Ubuntu) or libtirpc-devel (CentOS/Fedora)")
endif()


# # 找到 libtirpc
# find_path(TIRPC_INCLUDE_DIR NAMES rpc/rpc.h PATHS /usr/include/tirpc)
# find_library(TIRPC_LIB NAMES tirpc PATHS /usr/lib /usr/lib/x86_64-linux-gnu)

# if(TIRPC_INCLUDE_DIR AND TIRPC_LIB)
#     target_include_directories(sigar PUBLIC ${TIRPC_INCLUDE_DIR})
#     target_link_libraries(sigar PUBLIC ${TIRPC_LIB})
# else()
#     message(FATAL_ERROR "libtirpc not found. Did you install libtirpc-dev?")
# endif()