# cmake_minimum_required(VERSION 3.20)
# project(client_lib)

# ---------------- 源文件 ----------------
set(SRCS
    client_interface.cpp
    clientapp.cpp
    clientobjectbase.cpp
    config.cpp
    script_callbacks.cpp
    entity.cpp
    entity_aspect.cpp
    entity_component.cpp
    event.cpp
    moveto_point_handler.cpp
    profile.cpp
)
# ---------------- 创建静态库 ----------------
add_library(client_lib STATIC ${SRCS})

# ---------------- OpenSSL ----------------
target_link_libraries(client_lib PRIVATE KBEOpenSSL::SSL)

# ---------------- log4cxx ----------------

target_link_libraries(client_lib PUBLIC  log4cxx)
target_compile_definitions(client_lib PUBLIC  LOG4CXX_STATIC)


target_link_libraries(client_lib PUBLIC 
    helper
    xml
    fmt::fmt
    python_interface
)


