#!/bin/sh
set -e

cd ./kbe/src/
echo "[INFO] Starting build..."
cmake --build build -j4  -- VERBOSE=1

echo "[INFO] Step 3 complete 🎉"