from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext
from .forms import ReadWriteForm, UserLogInForm
from .write import writeData, readData, patronWrite
from .models import DeviceAndClientIp

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def checkPatron(data):
	import os
	cwd = os.getcwd()
	print(cwd)
	print("Hi")
	file = open("patrons.txt","r+")
	return 1 if data+"\n" in file.readlines() else 0

	file.close()

@login_required(login_url='/login/')
def readWriteView(request):
	readerIP = get_object_or_404(DeviceAndClientIp, client_ip = get_client_ip(request)).reader_ip
	readerPort = get_object_or_404(DeviceAndClientIp, client_ip = get_client_ip(request)).reader_port
	form = ReadWriteForm()
	a = ""
	context = {
		"myForm":form
	}
	form = ReadWriteForm(request.POST or None)
	if(request.POST):
		if '_PatronWrite' in request.POST:
			if checkPatron(request.POST['data']):
				a = patronWrite(request.POST['data'], readerIP, readerPort)
				messages.success(request, a)
				messages.success(request,"\n"+"User already got a rfid tag")
		elif '_BookWrite' in request.POST:
			a = writeData(request.POST['data'], readerIP, readerPort)
			messages.success(request, a)
		elif '_Read' in request.POST:
			a = readData(readerIP,readerPort)
			messages.success(request, a)
	return render(request, 'readwrite/index.html', context)

def userLoginView(request, *args, **kwargs):
    form = UserLogInForm(request.POST or None)
    print("Hello")
    if form.is_valid():
        username_ = form.cleaned_data.get('username')
        user_obj = User.objects.get(username__iexact=username_)
        login(request, user_obj)
        print ("logged in")
        return HttpResponseRedirect("/readwrite")
    return render(request, "accounts/login.html", {"form": form})

def userLogoutView(request):
    logout(request)
    return HttpResponseRedirect("/readwrite")

def homeView(request):
	return render(request, "accounts/base.html")
