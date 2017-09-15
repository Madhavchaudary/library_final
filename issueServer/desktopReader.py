import socket
import pymysql
import inspect
from .addLog import addLogFunc
#from . import constants
commands = 	{	'multiTagInventory': bytearray([10, 255, 2, 128, 117]), 
				'getTagData': bytearray([10, 255, 3, 65, 16, 163])
			}

def whoami():
    return inspect.stack()[1][3]

def sendCommand(cmd,ReaderIP, ReaderPort,s):
	s.send(cmd)
	raw_response = s.recv(2048)
	response = bytearray(raw_response)
	return raw_response


def getData(ReaderIP, ReaderPort):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.SOL_TCP)
		s.connect((ReaderIP, ReaderPort))
	except Exception as ex:
		addLogFunc(whoami(),str(ex))
		raise Exception('NetworkError: Socket creation failed.')
	try:	
		patron = ''
		books = []
		for i in range(15):
			response = sendCommand(commands['multiTagInventory'],ReaderIP, ReaderPort,s)
			count = response[5]	
			response = sendCommand(commands['getTagData'],ReaderIP, ReaderPort,s)[5:-1]
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
		addLogFunc(whoami(),str(ex))
		return ("One or more empty tags are present \n")

def Checkout(ReaderIP,ReaderPort):
	try:
		rfid_data = ''
		rfid_data = getData(ReaderIP, ReaderPort)	
		# db = pymysql.connect(constants.SQLHost, constants.SQLUser, constants.SQLPass, constants.SQLDB)
		# cardnumber = rfid_data['patron']	
		# cursor = db.cursor()
		# cursor.execute("""SELECT borrowernumber from borrowers WHERE cardnumber= %s""",(cardnumber,))
		# rfid_data['patron'] = cursor.fetchall()
		# db.close()
		return rfid_data
	except Exception as ex:
		addLogFunc(whoami(),str(ex))
		return "Some Error"

def Checkin(ReaderIP,ReaderPort):
	try:
		rfid_data = ''
		rfid_data = getData(ReaderIP, ReaderPort)['books']
		return rfid_data
	except Exception as ex:
		addLogFunc(whoami(),str(ex))
		return "Some Error"