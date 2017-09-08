from .desktopReader import Checkout,Checkin
from django.http import JsonResponse
from .models import device_info
def checkOutView(request, device_id):
	readerIP_ = device_info.objects.get(deviceID=device_id).readerIP
	readerPort_ = device_info.objects.get(deviceID=device_id).readerPort
	rfid_data = Checkout(readerIP_, readerPort_)
	print(readerPort_)
	return JsonResponse(rfid_data, safe=False)
def checkInView(request, device_id):
	readerIP_ = device_info.objects.get(deviceID=device_id).readerIP
	readerPort_ = device_info.objects.get(deviceID=device_id).readerPort

	rfid_data = Checkin(readerIP_, readerPort_)
	return JsonResponse(rfid_data, safe=False)