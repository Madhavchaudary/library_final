# #!/usr/bin/python2

# import socket
# import struct
# import time
# import MySQLdb
# from . import constants
# commands = 	{	'multiTagInventory': bytearray([10, 255, 2, 128, 117]), 
# 				'getTagData': bytearray([10, 255, 3, 65, 16, 163])
# 			}


# def sendCommand(cmd,readerIP, readerPort,s):
# 	s.send(cmd)
# 	raw_response = s.recv(2048)
# 	response = bytearray(raw_response)
# 	return raw_response


# def getData(readerIP, readerPort):
# 	try:
# 		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.SOL_TCP)
# 		s.connect((readerIP, readerPort))
# 	except:
# 		raise Exception('NetworkError: Socket creation failed.')
# 	patron = ''
# 	books = []
# 	for i in range(15):
# 		response = sendCommand(commands['multiTagInventory'],readerIP, readerPort,s)
# 		count = response[5]	
# 		response = sendCommand(commands['getTagData'],readerIP, readerPort,s)[5:-1]
# 		response = response[1:]
# 		for _ in range(count):
# 			response = response[1:]
# 			data = response[:12][::-1]
# 			response = response[13:]
# 			if ((bytearray(data[1]))==bytearray(b'')):
# 				raise Exception("WARNING: Attempted to read empty tag.")
# 			if (bytearray(data[0])) == bytearray(b'\x00'):
# 				data = data.decode()
# 				if patron == '':
# 					patron = ''.join([c if ord(c) != 0 else '' for c in data[1:]])
# 			else:
# 				data = data.decode()
# 				data = ''.join([c if ord(c) != 0 else '' for c in data])
# 				if data not in books:
# 					books += [data]
# 					print (books)	
# 	s.close()
# 	return {'patron':patron, 'books':books}

# def getBooksList(readerIP, readerPort):
# 	return getData(readerIP, readerPort)['books']


# def getPatronID(readerIP, readerPort):
# 	return getData(readerIP, readerPort)['patron']

# def getPatronIDAndBooksList(readerIP, readerPort):
# 	return getData(readerIP, readerPort)

# def Checkout(ReaderIP,ReaderPort):
# 	rfid_data = ''
# 	rfid_data = getPatronIDAndBooksList(ReaderIP,ReaderPort)
# 	db = MySQLdb.connect(constants.SQLHost, constants.SQLUser, constants.SQLPass, constants.SQLDB)
# 	cardnumber = rfid_data['patron']
# 	cursor = db.cursor()
# 	cursor.execute("""SELECT borrowernumber from borrowers WHERE cardnumber= %s""",(cardnumber,))
# 	rfid_data['patron'] = cursor.fetchall()
# 	db.close()
# 	return rfid_data

# def Checkin(ReaderIP,ReaderPort):
# 	rfid_data = ''
# 	rfid_data = getBooksList(ReaderIP,ReaderPort)	
# 	return rfid_data












#!/usr/bin/python2

import socket
import struct
import time
import MySQLdb
#from . import constants
commands = 	{	'multiTagInventory': bytearray([10, 255, 2, 128, 117]), 
				'getTagData': bytearray([10, 255, 3, 65, 16, 163])
			}

readerIP = "192.168.240.131"
readerPort = 100
def sendCommand(cmd,readerIP, readerPort,s):
	s.send(cmd)
	raw_response = s.recv(2048)
	response = bytearray(raw_response)
	return raw_response


def getData(readerIP, readerPort):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.SOL_TCP)
		s.connect((readerIP, readerPort))
	except:
		raise Exception('NetworkError: Socket creation failed.')
	try:	
		patron = ''
		books = []
		for i in range(15):
			response = sendCommand(commands['multiTagInventory'],readerIP, readerPort,s)
			count = response[5]	
			response = sendCommand(commands['getTagData'],readerIP, readerPort,s)[5:-1]
			response = response[1:]
			for _ in range(count):
				response = response[1:]
				data = response[:12][::-1]
				response = response[13:]
				if ((bytearray(data[1]))==bytearray(b'')):
					raise Exception("WARNING: Attempted to read empty tag.")
				if (bytearray(data[0])) == bytearray(b'\x00'):
					data = data.decode()
					if patron == '':
						patron = ''.join([c if ord(c) != 0 else '' for c in data[1:]])
				else:
					data = data.decode()
					data = ''.join([c if ord(c) != 0 else '' for c in data])
					if data not in books:
						books += [data]
						print (books)	
		s.close()
		return {'patron':patron, 'books':books}
	except Exception as ex:
		print("One or more empty tags are present")
		return ex

def getBooksList(readerIP, readerPort):
	return getData(readerIP, readerPort)['books']


def getPatronID(readerIP, readerPort):
	return getData(readerIP, readerPort)['patron']

def getPatronIDAndBooksList(readerIP, readerPort):
	return getData(readerIP, readerPort)






def Checkout(ReaderIP,ReaderPort):
	
	try:
		rfid_data = ''
		rfid_data = getPatronIDAndBooksList(ReaderIP,ReaderPort)	
#		db = MySQLdb.connect(constants.SQLHost, constants.SQLUser, constants.SQLPass, constants.SQLDB)
		cardnumber = rfid_data['patron']	
		#cursor = db.cursor()
		#cursor.execute("""SELECT borrowernumber from borrowers WHERE cardnumber= %s""",(cardnumber,))
		#rfid_data['patron'] = cursor.fetchall()
		#db.close()
		return rfid_data
	except:
		return "Some Error"

def Checkin(ReaderIP,ReaderPort):
	try:
		rfid_data = ''
		rfid_data = getBooksList(ReaderIP,ReaderPort)	
		return rfid_data
	except:
		return "Some Error"

# Checkin(readerIP,readerPort)
