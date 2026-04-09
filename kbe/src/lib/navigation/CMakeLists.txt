# ---------------- 源文件 ----------------
set(SRCS
	navigation.cpp
	navigation_handle.cpp
	navigation_tile_handle.cpp
	navigation_mesh_handle.cpp
)
# ---------------- 创建静态库 ----------------
add_library(navigation STATIC ${SRCS})



target_link_libraries(navigation PRIVATE fmt::fmt)
target_link_libraries(navigation PRIVATE RecastNavigation::Detour RecastNavigation::Recast RecastNavigation::DebugUtils RecastNavigation::DetourCrowd)

