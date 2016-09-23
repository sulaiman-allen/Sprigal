# Yomu
![](./imgs/Yomu%20Layout.jpg)
<br>
<br>
An Arduino based music player. Plays back audio file playlists based on the the rfid tag the program recieves (written in Python) matched to an entry in a Django database over the computer's serial port from an Arduino microcontroller. Uses the StrongLink [SL018](http://www.stronglink-rfid.com/en/rfid-modules/sl018.html) (13.56MHz Mifrare) RFID tag reader library. Also makes use of the pyserial library - http://pyserial.sourceforge.net/.
