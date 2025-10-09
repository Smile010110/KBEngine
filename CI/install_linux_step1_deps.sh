#!/bin/sh
set -e

# Detect distribution and select package manager
UPDATED=0
if command -v apt-get >/dev/null 2>&1; then
    INSTALL_CMD="sudo apt-get install -y"
    PKG_CHECK="dpkg -s"
    PKG_UPDATE="sudo apt-get update -y"
elif command -v dnf >/dev/null 2>&1; then
    INSTALL_CMD="sudo dnf install -y"
    PKG_CHECK="rpm -q"
    PKG_UPDATE="sudo dnf makecache -y"
elif command -v yum >/dev/null 2>&1; then
    INSTALL_CMD="sudo yum install -y"
    PKG_CHECK="rpm -q"
    PKG_UPDATE="sudo yum makecache -y"
elif command -v zypper >/dev/null 2>&1; then
    INSTALL_CMD="sudo zypper install -y"
    PKG_CHECK="rpm -q"
    PKG_UPDATE="sudo zypper refresh"
elif command -v pacman >/dev/null 2>&1; then
    INSTALL_CMD="sudo pacman -S --noconfirm --needed"
    PKG_CHECK="pacman -Qi"
    PKG_UPDATE="sudo pacman -Sy"
elif command -v apk >/dev/null 2>&1; then
    INSTALL_CMD="sudo apk add --no-cache"
    PKG_CHECK="apk info"
    PKG_UPDATE=""
else
    echo "[ERROR] Unknown package manager"
    exit 1
fi

update_pkg_index() {
    if [ "$UPDATED" -eq 0 ]; then
        if [ -n "$PKG_UPDATE" ]; then
            echo "[INFO] Updating package index..."
            $PKG_UPDATE || true
        fi
        UPDATED=1
    fi
}

install_dep() {
    NAME="$1"
    shift
    for PKG in "$@"; do
        if $PKG_CHECK "$PKG" >/dev/null 2>&1; then
            echo "[INFO] $NAME already installed ($PKG)"
            return 0
        fi
    done
    for PKG in "$@"; do
        echo "[INFO] Installing $NAME ($PKG)"
        if $INSTALL_CMD "$PKG" >/dev/null 2>&1; then
            echo "[INFO] Installed $PKG"
            return 0
        fi
    done
    echo "[WARN] Failed to install $NAME ($*)"
    return 1
}

update_pkg_index
install_dep "Git" git
install_dep "GCC" gcc g++ gcc-c++
install_dep "Make" make
install_dep "Autoconf" autoconf
install_dep "Libtool" libtool-bin libtool
install_dep "CMake" cmake
install_dep "pkg-config" pkg-config pkgconf
install_dep "curl" curl
install_dep "zip" zip
install_dep "unzip" unzip
install_dep "tar" tar
install_dep "TIRPC" libtirpc-dev libtirpc-devel
install_dep "MySQL/MariaDB" libmysqlclient-dev libmariadb-dev mariadb-devel mysql-devel
install_dep "libffi" libffi-dev libffi-devel
install_dep "UUID" uuid-dev libuuid-devel
install_dep "BZip2" libbz2-dev bzip2-devel
install_dep "OpenSSL" libssl-dev openssl-devel
install_dep "Zlib" zlib1g-dev zlib-devel
install_dep "CURL Dev" libcurl4-openssl-dev libcurl-devel

echo "[INFO] Step 1 complete ✅"