# ---------------- 源文件 ----------------
set(SRCS
    xml.cpp
)
# ---------------- 创建静态库 ----------------
add_library(xml STATIC ${SRCS})


target_link_libraries(xml PUBLIC 
    fmt::fmt
    tinyxml
)

