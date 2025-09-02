import socket,sys, random
from time import sleep
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#max_move=127
#min_move=-128
max_move=20
min_move=-20
def send_movement(data):
    #Convert data to bytes
    data = data.encode('utf-8')
    #send Data to mouse_filter.py 
    sock.sendto(data, ("127.0.0.1", 5928))
    print(f"AIM:{data}")
# x,y,l,r,scroll
#x="500"
#y="0"
#l="1"
#r="0"
#scr="0"
#Check for 5 arguments, script names counts as one soo checlk for 6 arguments
if len(sys.argv)!=6:
    exit()
# Start file like this to send aim:
# |_$_ send_aim.py x y l r scr
# sys.argv[0] is always the filename of this file with path 
x=int(sys.argv[1])
y=int(sys.argv[2])
l=int(sys.argv[3])
r=int(sys.argv[4])
scr=int(sys.argv[5])
# send_aim.py -40 -130 1 0 0
while x!=0 or y!=0:
    max_move=random.randint(4,15)
    min_move=-max_move
    step_x = max(min_move,min(max_move,x))
    step_y = max(min_move,min(max_move,y))
    data = str(step_x)+","+str(step_y)+",0,0,0"
    send_movement(data)
    x-=step_x
    y-=step_y
    #sleep 10 ms
    sleep(0.010)
#time.sleep(0.010) # 10 miliseconds wait
#Convert data to single string variable
#data = x+","+y+","+l+","+r+","+scr
#Convert data to bytes
#data = data.encode('utf-8')
#send Data to mouse_filter.py 
#sock.sendto(data, ("127.0.0.1", 5928))
#print(f"AIM:{x},{y},{l},{r},{scr}")