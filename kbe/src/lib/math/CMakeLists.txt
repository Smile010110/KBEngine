# ---------------- 源文件 ----------------
set(SRCS
	math.cpp
)
# ---------------- 创建静态库 ----------------
add_library(math STATIC ${SRCS})

target_link_libraries(math PRIVATE fmt::fmt)

