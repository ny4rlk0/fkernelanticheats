#!/bin/bash

# Exit immediately if any command fails
set -e
export PICO_SDK_PATH="/mnt/c/Users/user/.pico-sdk"
echo "🧹 Cleaning previous build..."
rm -rf build
mkdir build

echo "⚙️ Configuring CMake..."
cmake -G "Ninja" -S . -B build \
  -DCMAKE_SYSTEM_NAME=Generic \
  -DCMAKE_TRY_COMPILE_TARGET_TYPE=STATIC_LIBRARY \
  -DCMAKE_C_COMPILER=arm-none-eabi-gcc \
  -DCMAKE_CXX_COMPILER=arm-none-eabi-g++ \
  -DCMAKE_ASM_COMPILER=arm-none-eabi-gcc \
  -DCMAKE_C_FLAGS="-mcpu=cortex-m33 -mthumb" \
  -DCMAKE_CXX_FLAGS="-mcpu=cortex-m33 -mthumb" \
  -DCMAKE_ASM_FLAGS="-mcpu=cortex-m33 -mthumb" \
  -DPICO_BOARD=pico2_w \
  -DPICO_SDK_PATH="/mnt/c/Users/user/.pico-sdk"
#cmake -G "Ninja" -S . -B build \
#  -DCMAKE_TOOLCHAIN_FILE="/mnt/c/Users/user/.pico-sdk/external/pico_sdk_import.cmake" \
#  -DPICO_BOARD=pico_w \
#  -DPICO_SDK_PATH="/mnt/c/Users/user/.pico-sdk"
echo "🔨 Building project with Ninja..."
cmake --build build

echo "✅ Build complete. Output files:"
ls -lh build/blink.*
