from .desktopReader import Checkout,Checkin
from django.http import JsonResponse
from .models import device_info
def checkOutView(request, device_id):
	ip_addr = device_info.objects.get(device_id=device_id).device_ip
	rfid_data = Checkout(ip_addr, 100)
	return JsonResponse(rfid_data, safe=False)
def checkInView(request, device_id):
	ip_addr = device_info.objects.get(device_id=device_id).device_ip
	rfid_data = Checkin(ip_addr, 100)
	return JsonResponse(rfid_data, safe=False)