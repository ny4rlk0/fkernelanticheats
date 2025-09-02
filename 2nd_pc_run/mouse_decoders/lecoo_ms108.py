# LECOO MS108 SELECT USB GİRİŞ AYGITI or USB INPUT DEVICE FROM ZADIG THEN INSTALL DRIVER
vid, pid = 0x1BCF, 0x08A0
mouse_report_desc_byte_size = 7

def decode_mouse_report(data):
    if len(data) != mouse_report_desc_byte_size:
        print("Invalid report length")
        return None

    # Byte 0: Always 0x01 (report ID or constant)
    # Byte 1: Button bits
    l  = data[1] & 0x01          # Left click
    r  = (data[1] >> 1) & 0x01   # Right click
    m  = (data[1] >> 2) & 0x01   # Middle click
    b4 = (data[1] >> 3) & 0x01   # Extra button 2
    b5 = (data[1] >> 4) & 0x01   # Extra button 1
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
        #This mouse has buttons on left side lets ignore that
        #"b4": str(b4),
        #"b5": str(b5),
        "scr": str(scr),
        "x": str(x),
        "y": str(y)
    }