# LOGITECH G300S SELECT G300s Optical Gaming Mouse FROM ZADIG AND INTERFACE 0 INSTALL DRIVER
vid, pid = 0x046D, 0xC246
mouse_report_desc_byte_size = 8

def decode_mouse_report(data):
    if len(data) != mouse_report_desc_byte_size:
        print("Invalid report length")
        return None
    # Byte 0: Button states
    l = data[0] & 0x01          # Left click (0x01)
    r = (data[0] >> 1) & 0x01   # Right click (0x02)
    m = (data[0] >> 2) & 0x01   # Middle click (0x04)
    # Byte 2–3: X movement (little endian, signed)
    x = int.from_bytes(data[2:4], byteorder='little', signed=True)
    # Byte 4–5: Y movement (little endian, signed)
    y = int.from_bytes(data[4:6], byteorder='little', signed=True)
    # Byte 6: Scroll (signed byte)
    scr = data[6] - 256 if data[6] > 127 else data[6]
    return {
        "l": str(l),
        "r": str(r),
        "m": str(m),
        "scr": str(scr),
        "x": str(x),
        "y": str(y)
    }