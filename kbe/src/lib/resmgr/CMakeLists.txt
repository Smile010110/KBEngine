# ---------------- 源文件 ----------------
set(SRCS
	resmgr.cpp
	resourceobject.cpp
)
# ---------------- 创建静态库 ----------------
add_library(resmgr STATIC ${SRCS})


target_link_libraries(resmgr PRIVATE fmt::fmt)

