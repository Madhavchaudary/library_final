# file = open("logs.txt","r+")
# file.write("abc"+"\n")
# # if "abc" in file.read():
# 	# print("abc is not there")
# print("abc\n" in file.readlines())
# file.close()



def checkPatron(data):
	file = open("logs.txt","r+")
	return 1 if data+"\n" in file.readlines() else 0
	file.close()
print(checkPatron("abc"))
