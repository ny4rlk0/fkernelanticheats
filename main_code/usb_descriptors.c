#include "tusb_config.h"
#include "tusb.h"
#include "class/hid/hid_device.h"
#include "class/hid/hid.h"
#include "device/usbd.h"
#include <string.h>
#define CONFIG_TOTAL_LEN  (TUD_CONFIG_DESC_LEN + TUD_HID_DESC_LEN)
// Configuration Descriptor
#define ITF_NUM_TOTAL    1
#define EPNUM_MOUSE     0x81
#define ITF_NUM_MOUSE  0
//Index 0 is reserved for language ID and handled separately.
const char* string_desc_arr[] = { [1]="PixArt", [2]="Lenovo USB Optical Mouse" };
static uint16_t _desc_string[32];
//79 bytes LENOVO MOJUUO OEM MOUSE
static const uint8_t mouse_report_descriptor[]= {
0x05, 0x01, 
0x09, 0x02, 
0xA1, 0x01, 
0x09, 0x01, 
0xA1, 0x00, 
0x05, 0x09, 
0x19, 0x01, 
0x29, 0x03, 
0x15, 0x00, 
0x25, 0x01, 
0x75, 0x01,
0x95, 0x03, 
0x81, 0x02, 0x75, 0x05, 0x95, 0x01, 
0x81, 0x03, 0x06, 0x00, 0xFF, 0x09, 0x40, 0x95, 0x02, 0x75, 0x08, 0x15, 
0x81, 0x25, 0x7F, 
0x81, 0x02, 0x05, 0x01, 0x09, 0x38, 0x15, 
0x81, 0x25, 0x7F, 0x75, 0x08, 0x95, 0x01, 
0x81, 0x06, 0x09, 0x30, 0x09, 0x31, 0x16,
0x01, 0x80, 0x26, 0xFF, 0x7F, 0x75, 0x10, 0x95, 0x02, 
0x81, 0x06, 0xC0, 0xC0
};
#define DESC_MOUSE_SIZE sizeof(mouse_report_descriptor) // Size of the mouse report descriptor

// Device Descriptor
tusb_desc_device_t const desc_device = {
  .bLength            = sizeof(tusb_desc_device_t),
  .bDescriptorType    = TUSB_DESC_DEVICE,
  .bcdUSB             = 0x0200, // USB 2.0 = 0x0200 (High Speed), USB 1.1 = 0x0110(Full Speed), USB 1.0 = 0x0100 (Low Speed)
  .bDeviceClass       = 0x00,
  .bDeviceSubClass    = 0x00, // 0x01 = Boot Interface Subclass, 0x00 = No specific subclass
  // A boot mouse has to send 4 byte reports instead of 8 we are sending!
  .bDeviceProtocol    = 0x00, // 0x00 = No specific protocol (default),0x01 = Keyboard,  0x02 = Nouse
  .bMaxPacketSize0    = 0x08, // 64=0x40, 8=0x08 Max packet size for control endpoint
  .idVendor           = 0x17EF, // PixArt
  .idProduct          = 0x608D , // Lenovo USB Optical Mouse
  .bcdDevice          = 0x0100,
  .iManufacturer      = 0x01,
  .iProduct           = 0x02,
  .iSerialNumber      = 0x00, // No serial number
  .bNumConfigurations = 0x01
};
// USB Device Descriptor
uint8_t const desc_configuration[] = {
  TUD_CONFIG_DESCRIPTOR(1, ITF_NUM_TOTAL, 0, CONFIG_TOTAL_LEN, TUSB_DESC_CONFIG_ATT_REMOTE_WAKEUP, 100),
  TUD_HID_DESCRIPTOR(ITF_NUM_MOUSE, 0, false, DESC_MOUSE_SIZE, EPNUM_MOUSE, 8, 10), // 8 bytes max packet size, 10 ms polling interval
};
uint8_t const* tud_descriptor_device_cb(void) {
    return (uint8_t const*) &desc_device;
}

uint8_t const* tud_descriptor_device_qualifier_cb(void) {
    return NULL;  // High-speed not supported
}

uint8_t const* tud_descriptor_configuration_cb(uint8_t index) {
    (void)index;
    return desc_configuration;
}

uint16_t const* tud_descriptor_string_cb(uint8_t index, uint16_t langid) {
    //(void)langid;

    if (index == 0) {
        _desc_string[0] = (TUSB_DESC_STRING << 8) | 4;
        _desc_string[1] = 0x0409;
        return _desc_string;
    }

    if (index >= sizeof(string_desc_arr) / sizeof(string_desc_arr[0])) return NULL;

    const char* str = string_desc_arr[index];
    size_t len = strlen(str);
    if (len > 31) len = 31;

    _desc_string[0] = (TUSB_DESC_STRING << 8) | (2 * len + 2);
    for (size_t i = 0; i < len; i++) {
        _desc_string[1 + i] = str[i];//(uint16_t)str[i];
    }

    return _desc_string;
    //return tud_descriptor_string_cb(index, langid);
}
uint8_t const* tud_hid_descriptor_report_cb(uint8_t instance) {
    return mouse_report_descriptor;
}                      
/*uint16_t const* tud_descriptor_string_cb(uint8_t index, uint16_t langid) {
  return tud_string_descriptor_cb(index, langid);
}*/
/*const usb_hid_device_obj_t usb_hid_device_mouse_obj = {
    .base = {
        .type = &usb_hid_device_type,
    },
    .report_descriptor = mouse_report_descriptor,
    .report_descriptor_length = sizeof(mouse_report_descriptor),
    .usage_page = 0x01, // Generic Desktop Controls
    .usage = 0x02,      // Mouse
    .num_report_ids = 1,
    .report_ids = { 0x00, },
    .in_report_lengths = { 8, }, // 8 bytes for mouse report
    .out_report_lengths = { 0, },
};*/