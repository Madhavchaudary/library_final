import socket
def connect(readerIP,readerPort):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.SOL_TCP)
		s.connect((readerIP, readerPort))
		return s
	except:
		return (0)
# s = connect(readerIP,readerPort)
def writeData(data, readerIP, readerPort):
	s = connect(readerIP,readerPort)
	if s:
		try:
			print("WRITE DATA")
			if data == "":
				return "WARNING: PLEASE ENTER SOME DATA IN THE TEXT BOX"
			for i in range(12-len(data)):
				data = data + chr(0)
			for j in range(6):
				b2 = (data[j*2])
				b1 = (data[j*2+1])
				print("Writing 2 bytes")
				cmd = bytearray([10, 255, 10, 137, 0, 0, 0, 0, 1, 7 - j, ord(b1) ,ord(b2), CheckDigit(7-j, ord(b1), ord(b2))])
				s.send(cmd)
				out = s.recv(2048)
				print("Response: " + " ".join("%02x" % b for b in out))
			return readData(readerIP, readerPort)
		except Exception as ex:
			output = "Exception: " + str(ex)
			return (output)
	else:
		return ("CONNECTION ERROR: SOCKET CREATION FAILED")
def readData(readerIP, readerPort):
	s = connect(readerIP,readerPort)
	if s:
		try:
			print("Sending Read request.")
			cmd = bytearray([10, 255, 2, 128, 117])
			s.send(cmd)
			out = s.recv(2048)
			cnt = out[5]
			print("Response: " + " ".join("%02x" % b for b in out))

			print("Sending get tag data request.")
			cmd = bytearray([10, 255, 3, 65, 16, 163])
			s.send(cmd)
			out = s.recv(2048)
			print("Response: " + " ".join("%02x" % b for b in out))
			print(out)
			if out[4] > 1:
				return("WARNING: MORE THAN ONE TAGS IN RANGE")
			elif out[4] == 0:
				return("WARNING: NO TAGS IN RANGE!!!")
			out = out[7:7+12][::-1]
			if out[1] == 0x9e:
				return ("WARNING: EMPTY TAG IS PRESENT IN RANGE")
			out = out.decode()
			out = ''.join([c if ord(c) != 0 else '' for c in out])
			return (out)
		except Exception as ex:
			output = "Exception: " + str(ex)
			return (output)
	else:
		return ("CONNECTION ERROR: SOCKET CREATION FAILED")
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
def patronWrite(data1, readerIP, readerPort):
	s = connect(readerIP,readerPort)
	if s:
		try:
			data = chr(1) + data1
			ret = writeData(data, readerIP, readerPort)
			if data == chr(1):
				return ("WARNING: PLEASE ENTER SOME DATA IN THE TEXTBOX")

			if ret == data:
				return ("SUCCESS: WRITTEN "+ret)
			else:
				output = "PATRON WRITE NOT SUCCESSFUL"
				return (output)
		except Exception as ex:
			output = "Exception: " + str(ex)+"\n"
			return (output)
	else:
		return ("CONNECTION ERROR: SOCKET CREATION FAILED")