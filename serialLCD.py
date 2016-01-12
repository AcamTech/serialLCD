import serial
import time
import socket, struct, fcntl
import subprocess

#Open the serial port for the LCD
port = serial.Serial("/dev/ttyAMA0", baudrate=9600, bytesize=8, parity='N', stopbits=1,  timeout=3.0)

#Create a socket to use when figuring out IP addresses.
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockfd = sock.fileno()
SIOCGIFADDR = 0x8915

framebuffer = ['','']

#This function determines the IP address of an interface passed in.
def get_ip(iface = 'eth0'):
    ifreq = struct.pack('16sH14s', iface, socket.AF_INET, '\x00'*14)
    try:
        res = fcntl.ioctl(sockfd, SIOCGIFADDR, ifreq)
    except:
        return "Getting IP..."
    ip = struct.unpack('16sH2x4s8x', res)[2]
    return socket.inet_ntoa(ip)

def loop_string(framebuffer, num_cols, delay=0.3:
	padding = ' ' * num_cols
	s = padding + framebuffer[1] + padding
	for i in range(len[s] - num_cols + 1):
		framebuffer[1] = s[i:i+num_cols]
		port.write(framebuffer[0])
		port.write(framebuffer[1])
		time.sleep(delay)

# Main function (get IP addresses and write to screen.
def main():
	clearScreen()
	
	#Get IP of MusicBox
	currentIP = get_ip('eth0').rjust(16)
	framebuffer[0] = currentIP
	
	#Get Now Playing
	mpc = subprocess.Popen('mpc', stdout=subprocess.PIPE)
	head = subprocess.Popen('head -n1'.split(), stdin=mpc.stdout, stdout=subprocess.PIPE)
	mpc.stdout.close()
	out = head.communicate()[0]
	if out.startswith( 'volume' ):
		out = "Nothing playing"
	
	framebuffer[1] = out
	loop_string(framebuffer, 16)
	time.sleep(10)

	return

#setup, called once.
def setup():
	#setBacklight( 157 )
	clearScreen()
	return

#Clears the screen by resetting cursor and writing all spaces.
def clearScreen():
	port.write("\xFE\x01")
	port.write("                ")
	port.write("                ")
	port.write("\xFE\x01")
	return

#Set backlight level.
#Requires LCd reboot after wards (stops Rx-ing for some reason).
def setBacklight( val ):
	if val >= 128 and val <= 157 :
		port.write("\x7C")
		port.write(chr(val))
		print "Backlight set to:", val
	else:
		print "ERROR: Backlight not set:", val, "is an invalid value"
	return

#Run setup and infinite loop on main.
setup()
while True:
	main()
