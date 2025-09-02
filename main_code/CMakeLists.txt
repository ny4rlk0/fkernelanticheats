# == DO NOT EDIT THE FOLLOWING LINES for the Raspberry Pi Pico VS Code Extension to work ==
set(TINYUSB_OPT_OS OPT_OS_NONE CACHE STRING "Override TinyUSB OS setting")
if(WIN32)
    set(USERHOME $ENV{USERPROFILE})
else()
    set(USERHOME $ENV{HOME})
endif()
set(sdkVersion 2.1.1)
set(toolchainVersion 14_2_Rel1)
set(picotoolVersion 2.1.1)
set(picoVscode ${USERHOME}/.pico-sdk/cmake/pico-vscode.cmake)
if (EXISTS ${picoVscode})
    include(${picoVscode})
endif()
# ====================================================================================
#add_compile_options(-w)  # GCC/Clang: Suppresses all warnings
message(STATUS "Using compiler: ${CMAKE_C_COMPILER}")
cmake_minimum_required(VERSION 3.13)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
# Define project and SDK path
project(blink C CXX ASM)
set(PICO_SDK_PATH "${USERHOME}/.pico-sdk")
# Set board to raspberry pi pico w or pico 2 w
#set(PICO_BOARD pico2_w)
#set(PICO_BOARD pico_w)
# Pull in SDK setup
include(pico_sdk_import.cmake)
# Initialize SDK
pico_sdk_init()
# Define executable
add_executable(blink
    blink.c
	usb_descriptors.c
)
add_compile_definitions(CFG_TUSB_CONFIG_FILE=\"${PROJECT_SOURCE_DIR}/include/tusb_config.h\")
add_compile_definitions(CFG_TUSB_OS=OPT_OS_NONE)
# Set output name to elf ^-^ (*insert happy forest noises here*)
set_target_properties(blink PROPERTIES OUTPUT_NAME blink.elf)

# Include paths
target_include_directories(blink PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)
# Enable USB/UART
pico_enable_stdio_uart(blink 1)
pico_enable_stdio_usb(blink 1)
# Link dependencies
target_link_libraries(blink
	pico_stdlib
	pico_multicore
	hardware_watchdog
	hardware_gpio
	hardware_uart
	hardware_sync
	hardware_flash
	hardware_clocks
	tinyusb_device
	tinyusb_board
)
# Generate UF2/BIN/HEX
pico_add_extra_outputs(blink)