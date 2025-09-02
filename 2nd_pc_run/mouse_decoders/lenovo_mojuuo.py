# LENOVO OEM MOUSE MOJUUO SELECT LENOVO OPTICAL USB MOUSE FROM ZADIG THEN INSTALL DRIVER
vid,pid=0x17EF,0x608D
mouse_report_desc_byte_size=8
def decode_mouse_report(data):
    if len(data) != mouse_report_desc_byte_size:
        print("Invalid report length")
        return None
    #left_click, right_click, middle_click, vendor_1, vendor_2, scroll, dx, dy
    l=data[0] & 0x01
    r=(data[0] >> 1) & 0x01
    m=(data[0] >> 2) & 0x01
    scr=data[3] - 256 if data[3] > 127 else data[3]
    x=int.from_bytes(data[4:6], byteorder='little', signed=True)
    y=int.from_bytes(data[6:8], byteorder='little', signed=True)
    return {
        "l": str(l),
        "r": str(r),
        "m": str(m),
        "scr": str(scr),
        "x": str(x),
        "y": str(y)
    }