#pip install libusb1
#C:\Python313\python.exe -m pip install libusb1, pyserial
#import sys
#print(sys.executable)
#print(sys.path)
import usb1,serial,socket
import serial.tools.list_ports
from time import sleep
from multiprocessing import Value, sharedctypes, Lock
from threading import Thread
from ctypes import c_char, create_string_buffer
from queue import Queue
import random, math

sbaudrate=115200#9600 too slow
stimeout=100
sudpport=5928
inject_aim = Value('b', False)  # Boolean flag
aim_data_lock = Lock()
aim_data = sharedctypes.RawArray(c_char, 100)

serial_queue = Queue()

def serial_writer():
    global ser
    while True:
        cmd = serial_queue.get()
        try:
            ser.write(cmd.encode())
        except serial.SerialTimeoutException:
            print("Serial write timeout—dropping command:", cmd)
        except Exception as e:
            print("Serial error:", e)
def udp_listener(inject_aim, aim_data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", sudpport))
    while True:
        data, _ = sock.recvfrom(1024)
        print("UDP listener started on: 127.0.0.1:",sudpport)
        with aim_data_lock:
            data_bytes = data.decode()[:99].encode()
            aim_data[:len(data_bytes)] = data_bytes
            aim_data[len(data_bytes)] = 0  # null-terminate
            raw = bytes(aim_data[:]).split(b'\x00', 1)[0].decode('utf-8')
            parts = raw.split(",")
            if len(parts) == 5:
                x, y, l, r, scr = map(int, parts)
            print(f"aim_data.value: {raw}")
            print(f"aim_data.value V: {x},{y},{l},{r},{scr}")
        with inject_aim.get_lock():
            inject_aim.value = True
            print("inject_aim has set true!")
            #aim_injection(x,y,l,r,scr)
            send_movement(x, y, scroll=scr, right_click=r, soft_reset=0, left_click_duration=l)
            inject_aim.value = False
def send_movement(dx, dy, scroll=0, right_click=0, soft_reset=0, left_click_duration=0):
    cmd = f"{dx},{dy},{scroll},{right_click},{soft_reset},{left_click_duration}\n"
    if ser!= None:#ser.write(cmd.encode())
        serial_queue.put(cmd)
    else: print("Can't send command to pico serial is not connected!")
    #ser.close()
#    drivers               specific_mouse_driver  change this to your driver.
from mouse_decoders import lenovo_mojuuo as m
#from mouse_decoders import logitech_m330 as m
#from mouse_decoders import lecoo_ms108 as m
def return_report(data):
    return m.decode_mouse_report(data)
ctx = usb1.USBContext()
interrupt_interfaces = []
#vid,pid=0x1532,0x0098 # razer
#vid,pid=0x17EF,0x608D # lenovo oem
#vid,pid=0x1BCF,0x08A0 # lecoo
if __name__ == '__main__':
    Thread(target=serial_writer, daemon=True).start()
    Thread(target=udp_listener, args=(inject_aim, aim_data), daemon=True).start()
    i=0
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        print(f"{i}) {port.device} - {port.description}")
        i+=1
    # Ask user to choose COM PORT
    try:
        while True:
            user_index = input(f"\nEnter the number corresponding to your COM port (0–{i-1}): ")
            try: 
                user_index = int(user_index)
            except:
                continue
            if 0 <= user_index < len(ports):
                selected_port = ports[user_index].device
                # Open serial port (adjust 'COM4' or '/dev/ttyUSB0' to your actual port)
                # connect pico over serial
                try:ser = serial.Serial(port=selected_port, baudrate=sbaudrate, timeout=stimeout)
                except Exception as e:
                    print("Failed to open serial connection to port: ",selected_port,"\n",e)
                print(f"\nConnected to {selected_port}")
                break
            else:
                print("\nInvalid selection. Index out of range.")
    except ValueError:
        print("\nPlease enter a valid number.")
    for device in ctx.getDeviceList(skip_on_error=True):
        if device.getVendorID() == m.vid and device.getProductID() == m.pid:
            try:handle = device.open()
            except Exception as e:
                print("Error openning device: ",repr(e))
                exit()
            for config in device.iterConfigurations():
                for interface in config: 
                    for setting in interface:
                        interface_number = setting.getNumber()
                        print(f"Interface {interface_number}")
                        #try:
                        #    handle.claimInterface(interface_number)
                        #except usb1.USBError as e:
                        #    print("!ERROR CLAMING INTF!:",e)
                        for endpoint in setting:
                            ep_type = endpoint.getAttributes() & 0x3  # Bits 0–1 define transfer type
                            is_in = endpoint.getAddress() & 0x80
                            type_names = ["Control", "Isochronous", "Bulk", "Interrupt"]
                            packet_size = endpoint.getMaxPacketSize()
                            #print(f"Max packet size: {packet_size}")
                            #print(f"Endpoint: {hex(endpoint.getAddress())}, Type: {type_names[ep_type]}")
                            if ep_type ==3 and is_in:
                                print(f"Found Interrupt IN on Interface {interface_number}, Endpoint: {hex(endpoint.getAddress())}")
                                interrupt_interfaces.append((interface_number, endpoint.getAddress()))
            last_error=""
            handle.claimInterface(0)
            while True:
                try:
                    mouse_report_binary= handle.interruptRead(0x81, m.mouse_report_desc_byte_size, timeout=100)  #100ms timeout
                    #print(f"RAW Mouse data: \n {mouse_report_binary}")
                    report=return_report(mouse_report_binary)
                    l = int(report["l"])
                    r = int(report["r"])
                    mid = int(report["m"])
                    scr = int(report["scr"])
                    x = int(report["x"])
                    y = int(report["y"])
                    send_movement(x,y,scroll=scr,right_click=r,soft_reset=0,left_click_duration=l)
                    #print("Decoded Mouse Data: ",report)
                    print(f"X: {x} | Y: {y}")
                    #print(f"\nDecoded Mouse Data: \n X: {x}\n Y: {y}\n Scroll: {scr}\n Right Click: {r}\n Left Click: {l}\n")
                except usb1.USBError as e:
                    current_error = repr(e)
                    if current_error!=last_error and current_error!="USBErrorTimeout()":
                        print("!ERROR!: ",repr(e))
                        last_error = repr(e)
                    else: pass