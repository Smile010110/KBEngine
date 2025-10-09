#!/bin/sh
set -e

KBE_CONFIG=${1:-Release}
VCPKG_DIR="$HOME/kbe-vcpkg"

echo "[INFO] Checking vcpkg..."
if [ ! -d "$VCPKG_DIR" ]; then
    git clone https://github.com/microsoft/vcpkg.git "$VCPKG_DIR"
fi

cd "$VCPKG_DIR"
./bootstrap-vcpkg.sh
cd -

echo "[INFO] Running cmake configure"
cd ./kbe/src/
cmake -B build -S . \
    -DCMAKE_TOOLCHAIN_FILE="$VCPKG_DIR/scripts/buildsystems/vcpkg.cmake" \
    -DKBE_CONFIG="$KBE_CONFIG"

echo "[INFO] Step 2 complete ✅"