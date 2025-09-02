# fuckkernelanticheats
Always Running Kernel Anti Cheats shouldn't have been existed! This makes them useless! Players will always find a ways to cheat. This doesn't excuse running AC at kernel level at all times (i am looking at you 4 letter company), starting ac from boot or invading other people's privacy!
![IMG](https://raw.githubusercontent.com/ny4rlk0/fuckkernelanticheats/refs/heads/main/picture.png)
The Pico 2 W appears as a real USB mouse on the computer you plug it into, <br>
while receiving mouse movements from the second <br>
computer via the UART using the Type-C UART CP2102 shown in the image. <br>
I wrote a demo Python code for this.<br>
<br>
The firmware is only compatible with certain mouse models. <br>
It has currently been tested with the Logitech M330 and Lecoo MS108.<br>
High-speed or complex gaming mice may not be supported.<br>
<br>
(The mouse will not support mice with a report descriptor greater than 8 bytes or faster than 1000Hz.)<br>
<br>
Currently, it only supports the Logitech m330 or Lecoo ms108 as a mouse. <br>
You can develop the demo software and add your own mouse, but not every mouse will work. <br>
Gaming mice with multiple interfaces or buttons from Razer, Logitech, etc. will not work. <br>
Mice with a single interface have a higher chance of working. <br>
The Python code is provided solely as an example to help you understand how to use the firmware. <br>
<br>
Required hardware:<br>
<br>
* 1 supported mouse.
* 1 Raspberry Pi Pico 2W
* 1 CP2102 Type C UART or other UART device that supports 115200<br>
* 3 Female-to-Female Jumper Cables<br>
* 1 Micro USB Cable<br>
* 1 Type C Cable<br>
<br>
Cable Connections:<br>
<br>
Pico 2W GP0 => CP 2102 RXD (Orange Wire in the picture) <br>
Pico 2W GP1 => CP 2102 TXD (Yellow Wire in the picture) <br>
Pico 2W GND => CP 2102 GND (Green Wire in the picture) <br>
<br>
Silicon Labs CP2102 UART Installation:
<br>
Remove the Yellow Jumper Switch on the CP2102 and reconnect it, covering VCCIO and 5V, as shown in the picture. <br>
Doing this incorrectly could damage the board by supplying 5V to the 3V circuit. <br>
Install the Silicon Labs CP2102 driver on the UART COM port connected to the second computer via Device Manager. <br>
Set the UART Speed ​​to 115200 in Device Manager. <br>
<br>
The General Logic is as follows:<br>
<br>
The PICO 2 W introduces itself as a legit HID mouse to the gaming computer.<br>
The PICO 2 W receives mouse commands from the second computer via the UART (SL CP2102).<br>
You connect a supported mouse to the second computer and install the WinUSB driver for it using Zadig.<br>
Uncomment the mouse you want to support in the mouse_filter.py file.<br>
With a supported mouse connected, run the mouse_filter.py file and select the correct COM port.<br>
Mouse movements made from the second computer are transferred via UART to the PICO 2 W, which appears <br>
as a mouse on the first gaming computer. This does not affect the second computer's mouse.<br>
You can either record the first computer with OBS, watch the screen from the second computer,<br>
and aim with any device or software. You can send this aim using the example in the send_aim.py file. <br>
Or, you can use a Screen Recorder card without displaying the first computer's image<br>
output to the monitor and connect its USB output to the second computer.<br>
Aim with any device or software.<br>
You can send the aim with the send_aim.py file.<br>
<br>
Note about send.aim.py: The information entered here is sent directly from the pico 2 W to the first gaming computer as a mouse descriptor report. <br>
<br>
If the transmitted movement is too fast, you may trigger Anti-Cheat's Inhuman Movement feature. <br>
This means if your mouse travels a ridiculous distance, like 20 meters, you could encounter a problem. <br>
Slow down, smooth out, and add slight errors before sending the movement. Don't send too much movement all at once! <br> 
The firmware limits the mouse's x and y movements to 128. This is sufficient for a proper software and device. <br>
