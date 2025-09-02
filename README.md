# fuckkernelanticheats
⚠️ For educational and research purposes only. This project critiques invasive anti-cheat practices, especially those operating at kernel level and violating user privacy.<br>
<br>
💡 MIT Licensed. No binaries, no injection, no modification. Just pure hardware emulation.<br>
If they ban this mouse just emulate different mouse you can change this from blink.c/usb_descriptors.c. They can't block this permanently at all!<br>
<br>
There shouldn't be Kernel Anti-Cheat programs running all the time! Players always find a way to cheat. That doesn't excuse always running AC at the kernel level, starting AC before the OS, or violating other people's privacy!
![IMG](https://raw.githubusercontent.com/ny4rlk0/fkernelanticheats/refs/heads/main/picture.png)
![IMG](https://raw.githubusercontent.com/ny4rlk0/fkernelanticheats/refs/heads/main/picture2.png)
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

# Türkçe

⚠️ Yalnızca eğitim ve araştırma amaçlıdır. Bu proje, özellikle çekirdek düzeyinde çalışan ve kullanıcı gizliliğini ihlal eden müdahaleci hile önleme uygulamalarını eleştirmektedir.

💡 MIT Lisanslı. İkili dosya yok, enjeksiyon yok, değişiklik yok. Sadece saf donanım emülasyonu.

Sürekli çalışan Çekirdek Hile Önleme programları olmamalı! Oyuncular her zaman hile yapmanın bir yolunu bulur. Bu, AC'yi her zaman çekirdek düzeyinde çalıştırmayı, AC'yi işletim sisteminden önce başlatmayı veya başkalarının gizliliğini ihlal etmeyi mazur göstermez! IMG Pico 2 W, taktığınız bilgisayarda gerçek bir USB fare gibi görünürken, görselde gösterilen Type-C UART CP2102'yi kullanarak ikinci bilgisayardan UART aracılığıyla fare hareketlerini alır.
Bunun için bir demo Python kodu yazdım.

Ürün yazılımı yalnızca belirli fare modelleriyle uyumludur.
Şu anda Logitech M330 ve Lecoo MS108 ile test edilmiştir.
Yüksek hızlı veya karmaşık oyun fareleri desteklenmeyebilir.

(Fare, 8 bayttan büyük veya 1000 Hz'den hızlı bir rapor tanımlayıcısına sahip fareleri desteklemez.)

Şu anda yalnızca Logitech m330 veya Lecoo ms108 farelerini destekler.
Demo yazılımını geliştirip kendi farenizi ekleyebilirsiniz, ancak her fare çalışmayacaktır.
Razer, Logitech vb. markaların birden fazla arayüzü veya düğmesi olan oyun fareleri çalışmayacaktır.
Tek arayüzlü farelerin çalışma olasılığı daha yüksektir.
Python kodu, yalnızca ürün yazılımının nasıl kullanılacağını anlamanıza yardımcı olmak için örnek olarak verilmiştir.

Gerekli donanım:

* 1 adet desteklenen fare. 1 Raspberry Pi Pico 2W
* 1 CP2102 Type C UART veya 115200'ü destekleyen başka bir UART cihazı
* 3 Dişi-Dişi Jumper Kablosu
* 1 Mikro USB Kablosu
* 1 Type C Kablosu

Kablo Bağlantıları:<br>

Pico 2W GP0 => CP 2102 RXD (Resimdeki Turuncu Kablo)<br>
Pico 2W GP1 => CP 2102 TXD (Resimdeki Sarı Kablo)<br>
Pico 2W GND => CP 2102 GND (Resimdeki Yeşil Kablo)<br>

Silicon Labs CP2102 UART Kurulumu:
CP2102 üzerindeki Sarı Jumper Anahtarını çıkarın ve resimde gösterildiği gibi VCCIO ve 5V'u kapatacak şekilde yeniden bağlayın.
Bunu yanlış yapmak, 3V devresine 5V vererek karta zarar verebilir. Silicon Labs CP2102 sürücüsünü Aygıt Yöneticisi aracılığıyla ikinci bilgisayara bağlı UART COM portuna yükleyin.
Aygıt Yöneticisi'nde UART Hızını 115200 olarak ayarlayın.

Genel Mantık şu şekildedir:

PICO 2 W, oyun bilgisayarına kendini gerçek bir HID fare olarak tanıtır.
PICO 2 W, ikinci bilgisayardan UART (SL CP2102) aracılığıyla fare komutlarını alır.
Desteklenen bir fareyi ikinci bilgisayara bağlayın ve Zadig kullanarak WinUSB sürücüsünü yükleyin.
mouse_filter.py dosyasında desteklemek istediğiniz farenin açıklamasını kaldırın.
Desteklenen bir fare bağlıyken, mouse_filter.py dosyasını çalıştırın ve doğru COM portunu seçin.
İkinci bilgisayardan yapılan fare hareketleri, UART aracılığıyla ilk oyun bilgisayarında fare olarak görünen PICO 2 W'ye aktarılır. Bu, ikinci bilgisayarın faresini etkilemez. İlk bilgisayarı OBS ile kaydedebilir, ikinci bilgisayardan ekranı izleyebilir ve herhangi bir cihaz veya yazılımla nişan alabilirsiniz. Bu nişanı send_aim.py dosyasındaki örneği kullanarak gönderebilirsiniz.
Ya da, ilk bilgisayarın görüntü çıkışını monitöre göstermeden bir Ekran Kaydedici kartı kullanabilir ve USB çıkışını ikinci bilgisayara bağlayabilirsiniz.
Herhangi bir cihaz veya yazılımla nişan alın.
Nişanı send_aim.py dosyasıyla gönderebilirsiniz.

send.aim.py hakkında not: Buraya girilen bilgiler, doğrudan pico 2 W'den ilk oyun bilgisayarına fare tanımlayıcı raporu olarak gönderilir.

İletilen hareket çok hızlıysa, Anti-Cheat'in İnsanlık Dışı Hareket özelliğini tetikleyebilirsiniz.
Bu, fareniz 20 metre gibi saçma bir mesafe kat ederse bir sorunla karşılaşabileceğiniz anlamına gelir.
Hareket göndermeden önce yavaşlatın, yumuşatın ve küçük hatalar ekleyin. Tek seferde çok fazla hareket göndermeyin! Yazılım, farenin x ve y hareketlerini 128 ile sınırlandırıyor. Bu, düzgün bir yazılım ve cihaz için yeterli.
