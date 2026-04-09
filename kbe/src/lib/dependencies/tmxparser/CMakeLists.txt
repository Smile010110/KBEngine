# 源文件列表
set(SRCS
	base64.cpp
	TmxEllipse.cpp
	TmxImage.cpp
	TmxImageLayer.cpp
	TmxLayer.cpp
	TmxMap.cpp
	TmxObject.cpp
	TmxObjectGroup.cpp
	TmxPolygon.cpp
	TmxPolyline.cpp
	TmxPropertySet.cpp
	TmxTile.cpp
	TmxTileset.cpp
	TmxUtil.cpp
)

# 生成静态库
add_library(tmxparser STATIC ${SRCS})

# 如果没传入 KBE_ROOT，则默认取上级目录
if(NOT DEFINED KBE_ROOT)
    set(KBE_ROOT ${CMAKE_SOURCE_DIR}/../..) 
endif()





# 在这里声明依赖 tinyxml
target_link_libraries(tmxparser PUBLIC tinyxml)

target_link_libraries(tmxparser
    PRIVATE fmt::fmt
)