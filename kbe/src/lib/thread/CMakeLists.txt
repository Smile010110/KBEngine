# ---------------- 源文件 ----------------
set(SRCS
	threadpool.cpp
	concurrency.cpp
)
# ---------------- 创建静态库 ----------------
add_library(thread STATIC ${SRCS})


target_link_libraries(thread PRIVATE fmt::fmt)

