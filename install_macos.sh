#!/usr/bin/env bash
set -e

echo ">>> 暂未适配"
# # ==============================
# # 安装 KBEngine-Nex (macOS 版本)
# # ==============================

# # 默认构建类型（可通过参数覆盖）
# KBE_CONFIG=${1:-Release}

# echo ">>> 使用构建类型: $KBE_CONFIG"


# # ------------------------------
# # 0. 检查并安装 Xcode Command Line Tools
# # ------------------------------
# if ! xcode-select -p >/dev/null 2>&1; then
#     echo ">>> 安装 Xcode Command Line Tools"
#     xcode-select --install
#     echo "请完成安装后重新运行本脚本"
#     exit 1
# fi
# echo ">>> 已检测到 Xcode Command Line Tools"

# # ------------------------------
# # 1. 检查系统版本
# # ------------------------------
# MACOS_VERSION=$(sw_vers -productVersion | cut -d'.' -f1)
# if [ "$MACOS_VERSION" -lt 11 ]; then
#     echo "错误: 需要 macOS 11.0 (Big Sur) 或更高版本，当前版本: $MACOS_VERSION"
#     exit 1
# fi
# echo ">>> 系统版本检查通过: macOS $MACOS_VERSION"

# # ------------------------------
# # 2. 确认 brew 已安装
# # ------------------------------
# if ! command -v brew >/dev/null 2>&1; then
#     echo "错误: 未检测到 Homebrew，请先安装: https://brew.sh/"
#     exit 1
# fi

# # ------------------------------
# # 3. 安装依赖
# # ------------------------------
# BREW_DEPS=(
#     autoconf
#     libtirpc
#     cmake
#     pkg-config
#     libffi
#     ossp-uuid
# )

# for pkg in "${BREW_DEPS[@]}"; do
#     if ! brew ls --versions "$pkg" >/dev/null 2>&1; then
#         echo ">>> 安装 $pkg"
#         brew install "$pkg"
#     else
#         echo ">>> 已安装 $pkg"
#     fi
# done

# # 注意：brew 装的 mysql-client 可能需要手动配置链接
# # if [ -d "$(brew --prefix mysql-client)" ]; then
# #     export PATH="$(brew --prefix mysql-client)/bin:$PATH"
# #     export LDFLAGS="-L$(brew --prefix mysql-client)/lib $LDFLAGS"
# #     export CPPFLAGS="-I$(brew --prefix mysql-client)/include $CPPFLAGS"
# #     echo ">>> 已配置 mysql-client 路径"
# # fi

# # ------------------------------
# # 4. vcpkg
# # ------------------------------
# VCPKG_DIR=~/kbe-vcpkg
# if [ ! -d "$VCPKG_DIR" ] || [ ! -f "$VCPKG_DIR/bootstrap-vcpkg.sh" ]; then
#     echo ">>> 克隆并安装 vcpkg"
#     git clone https://github.com/microsoft/vcpkg.git "$VCPKG_DIR"
# else
#     echo ">>> vcpkg 已存在: $VCPKG_DIR"
# fi

# OLDPWD=$(pwd)
# cd "$VCPKG_DIR"
# ./bootstrap-vcpkg.sh
# cd "$OLDPWD"

# # ------------------------------
# # 5. 构建 KBEngine-Nex
# # ------------------------------
# echo ">>> ./kbe/src/"
# cd "./kbe/src/"

# echo ">>> 配置 CMake"
# cmake -B build -S . \
#     -DCMAKE_TOOLCHAIN_FILE=$VCPKG_DIR/scripts/buildsystems/vcpkg.cmake \
#     -DKBE_CONFIG=$KBE_CONFIG

# echo ">>> 开始编译 KBEngine-Nex"
# cmake --build build -j$(sysctl -n hw.ncpu)

# echo ">>> 安装完成 🎉"
