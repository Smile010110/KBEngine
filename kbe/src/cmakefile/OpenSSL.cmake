# cmake/FindOrBuildOpenSSL.cmake
# 自动查找系统 OpenSSL 或使用自带 OpenSSL，并创建 INTERFACE 库 KBEOpenSSL::SSL

# 优先查找系统 OpenSSL
find_package(OpenSSL QUIET)

if(OpenSSL_FOUND)
    set(USE_SELF_OPENSSL 0)
    set(OPENSSL_INCLUDE_DIRS ${OPENSSL_INCLUDE_DIR})
    set(OPENSSL_LIBRARIES ${OPENSSL_LIBRARIES})
    message(STATUS "Using system OpenSSL: ${OPENSSL_VERSION}")
else()
    set(USE_SELF_OPENSSL 1)
    set(OPENSSL_DIR "${KBE_ROOT}/kbe/src/lib/dependencies/openssl")
    set(OPENSSL_INCLUDE_DIRS "${OPENSSL_DIR}/include")
    set(OPENSSL_LIBRARIES ssl crypto dl)
    message(WARNING "System OpenSSL not found, using self-built OpenSSL in ${OPENSSL_DIR}")
endif()

# 创建 INTERFACE 库
add_library(KBEOpenSSL::SSL INTERFACE IMPORTED)
set_target_properties(KBEOpenSSL::SSL PROPERTIES
    INTERFACE_INCLUDE_DIRECTORIES "${OPENSSL_INCLUDE_DIRS}"
    INTERFACE_LINK_LIBRARIES "${OPENSSL_LIBRARIES}"
    INTERFACE_COMPILE_DEFINITIONS "USE_OPENSSL"
)