#!/usr/bin/python3
import socket
import sys
import time
readerIP = "192.168.240.131"
readerPort = 100
#connect to rfid reader
def connect(readerIP, readerPort):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.SOL_TCP)
		s.connect((readerIP, readerPort))
		return s
	except socket.error as ex:
		# output = "Socket Creation failed"
		return(ex)

#send the reader a read request to check for multiple tags and stop the execution of the function "writeData" if multiple tags are foung
def readRequest(s):
	cmd = bytearray([10, 255, 2, 128, 117])
	s.send(cmd)
def getData(s):
	readRequest(s)
	cmd = bytearray([10, 255, 3, 65, 16, 163])
	s.send(cmd)
	return s.recv(2048)
def CheckDigit(a, b, c):
	i = a + b + c + 413
	if i < 255:
		i = 256 - i
	elif i < 511:
		i = 512 - i
	elif i < 1023:
		i = 1024 - i
	if i > 255:
		i = i - 256
	return i
def sendWriteRequest(data, s):
	for i in range(12-len(data)):
		data = data + chr(0)
	for j in range(6):
		b2 = (data[j*2])
		b1 = (data[j*2+1])
		# Sending Write request... 10,255,10,137,0,0,0,0,1, 7 - position to write in, byte1, byte2, CheckDigitValue
		print("Writing 2 bytes")
		cmd = bytearray([10, 255, 10, 137, 0, 0, 0, 0, 1, 7 - j, ord(b1) ,ord(b2), CheckDigit(7-j, ord(b1), ord(b2))])
		s.send(cmd)
		# Reading response...
		out = s.recv(2048)
		return out
# made two functions readDataAfterWrite and readData as some errors will be captured before reading in writeData function
# needed slight duplication 
def readDataAfterWrite(s, readerIP, readerPort):
	print ("Reading data after write")
	try:
		out = getData(s)
		if out == b'\x0b\x83\x11\x00\x01\r\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01R':
			return ("'WARNING:NO TAG IS PRESENT' OR 'PLEASE ENTER SOME DATA IN THE TEXTBOX'")
		out = out[7:7+12][::-1]
		if out == b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00':
			return("WARNING: 'ATTEMPTED TO READ AN EMPTY TAG' or 'PLEASE ENTER SOME DATA IN THE TEXTBOX'")
		out = out.decode()
		out = ''.join([c if ord(c) != 0 else '' for c in out])
		return (out)
	except Exception as ex:
		return (ex)
def writeData(data, readerIP, readerPort):
	print("WRITE DATA")
	s = connect(readerIP, readerPort)
	try:
		out = getData(s)
		print(out)
		if out[4] > 1 :
			return("WARNING: MORE THAN ONE TAGS IN RANGE")#stops the execution of this function if more than one tags are found
		out = sendWriteRequest(data, s)
		if out[3] == 82:
			return('WARNING: NO TAG IS PLACED ON THE WRITER.')	#happened when no tag was there on the device.
		return readDataAfterWrite(s, readerIP, readerPort)
	except Exception as ex:
		return (ex)
def readData(readerIP, readerPort):
	print ("Reading data")
	s = connect(readerIP, readerPort)
	try:
		out = getData(s)
		if out[4] > 1 :
			return("WARNING: MORE THAN ONE TAGS IN RANGE")
		elif out == b'\x0b\x83\x11\x00\x01\r\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01R':
			return ("'WARNING:NO TAG IS PRESENT' OR 'PLEASE ENTER SOME DATA IN THE TEXTBOX'")
		elif out[4] == 0:
			return("WARNING: NO TAGS IN RANGE")
		out = out[7:7+12][::-1]
		if out == b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00':
			return("WARNING: 'ATTEMPTED TO READ AN EMPTY TAG' or 'PLEASE ENTER SOME DATA IN THE TEXTBOX'")
		out = out.decode()
		out = ''.join([c if ord(c) != 0 else '' for c in out])
		return (out)
	except Exception as ex:
		return (ex)	
def patronWrite(data1, readerIP, readerPort):
	try:
		data = chr(1) + data1
		ret = writeData(data, readerIP, readerPort)
		if data == chr(1):
			return ("'WARNING:NO TAG IS PRESENT' OR 'PLEASE ENTER SOME DATA IN THE TEXTBOX'")
		if ret == data:
			output = "\nSUCCESSFULLY WROTE " + ret
			return (output)			
		else:
			output = "WRITE ERROR! Debug: Wrote " + ret
			return (output)
	except Exception as ex:
		output = "Internal Exception: " + str(ex)
		return (output)
