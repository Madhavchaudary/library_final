import time
time = time.localtime()
def addLogFunc(functionName,exceptionData):
	file = open("islogs.txt","a+")
	file.write(str(time.tm_mday)+":"+str(time.tm_mon)+":"+str(time.tm_year)+"   "+str(time.tm_hour)+":"+str(time.tm_min)+":"+str(time.tm_sec)+"\n")
	file.write("In function: "+functionName+"\n"+exceptionData+"\n")
	file.write("".join(["_" for _ in range(50)])+"\n")
