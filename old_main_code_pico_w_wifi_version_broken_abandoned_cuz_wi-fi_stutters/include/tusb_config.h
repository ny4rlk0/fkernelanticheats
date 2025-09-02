#ifndef _TUSB_CONFIG_H_
#define _TUSB_CONFIG_H_

#ifndef CFG_TUSB_OS
#define CFG_TUSB_OS OPT_OS_NONE
#endif

//--------------------------------------------------------------------+
// Supported OS Gözatman için:
//--------------------------------------------------------------------+

/*
#define OPT_OS_NONE       1  ///< No RTOS
#define OPT_OS_FREERTOS   2  ///< FreeRTOS
#define OPT_OS_MYNEWT     3  ///< Mynewt OS
#define OPT_OS_CUSTOM     4  ///< Custom OS is implemented by application
#define OPT_OS_PICO       5  ///< Raspberry Pi Pico SDK
#define OPT_OS_RTTHREAD   6  ///< RT-Thread
#define OPT_OS_RTX4       7  ///< Keil RTX 4
*/

#define STR_HELPER(x) #x
#define STR(x) STR_HELPER(x)

#pragma message("🔧[CFG_TUSB_OS SET] File: " __FILE__ ", Line: " STR(__LINE__) ", Value: " STR(CFG_TUSB_OS))

//--------------------------------------------------------------------+
#ifndef CFG_TUD_HID
#define CFG_TUD_HID 1
#endif

#ifndef CFG_TUD_ENABLED
#define CFG_TUD_ENABLED 1
#endif

#ifndef CFG_TUSB_DEBUG
#define CFG_TUSB_DEBUG 0
#endif

#ifndef CFG_TUD_VENDOR
#define	CFG_TUD_VENDOR 0
#endif

#ifndef CFG_TUD_CDC
#define	CFG_TUD_CDC 1
#endif

#ifndef CFG_TUSB_RHPORT0_SPEED
#define CFG_TUSB_RHPORT0_SPEED OPT_SPEED_FULL
#endif
#define CFG_TUD_CDC_EP_BUFSIZE 8
#define CFG_TUSB_MEM_ALIGN __attribute__ ((aligned(8)))
#define CFG_TUD_ENDPOINT0_SIZE 8
#define CFG_TUD_HID_EP_BUFSIZE 8

#ifndef CFG_TUD_MSC
#define	CFG_TUD_MSC 0
#endif

#ifndef CFG_TUD_MIDI
#define	CFG_TUD_MIDI 0
#endif

#ifndef CFG_TUSB_MCU
#define	CFG_TUSB_MCU OPT_MCU_RP2040
#endif

#ifndef CFG_TUSB_RHPORT0_MODE
#define	CFG_TUSB_RHPORT0_MODE OPT_MODE_DEVICE
#endif

#ifndef CFG_TUSB_RHPORT0_NUM
#define CFG_TUSB_RHPORT0_NUM 0
#endif

#endif