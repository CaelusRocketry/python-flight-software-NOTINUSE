import packet
import heapq
import socket
import tcp_socket
import subprocess

def interpret(packet):
	try:
		return(eval(packet.message))
	except:
		return("ERROR")
def get_ip():
	return(subprocess.getoutput("hostname -I").split()[1])

def get_core_temp():
	#return(subprocess.getoutput("/opt/vc/bin/vcgencmd measure_temp"))
	return("48.0 C")

def get_core_speed():
	#return(subprocess.getoutput("lscpu | grep MHz").split()[1]+" MHz")
	return("1.400 MHz")

def abort():
	return("ABORTING")
