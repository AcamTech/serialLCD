serialLCD
=========

Writes IP addresses to Sparkfun Serial LCD on a Raspberry Pi. Also modified to work with Pi MusicBox to scroll "Now Playing".

IP is set on the first row of he LCD panel and the second row will show/scroll what is currently playing on the Pi MusicBox.

Install rpi-serial-console and use it to disable the default serial console.
https://github.com/lurch/rpi-serial-console

sudo rpi-serial-console disable

Install python-serial
sudo apt-get install python-serial

Setup a cron job for the script
sudo crontab -e
add a line: @reboot python /home/pi/serialLCD/serialLCD.py &

Reboot.

The IP address code is from this SO post: http://stackoverflow.com/a/9267833
