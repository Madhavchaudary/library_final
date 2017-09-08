from django.db import models
class device_info(models.Model):
	deviceID = models.CharField(max_length=20)
	readerIP = models.GenericIPAddressField(default=None)
	readerPort = models.IntegerField(default=100, null=True)
	def __str__(self):
		return str("Device ID = "+self.deviceID +"		Reader IP = "+self.readerIP)
	def __unicode__(self):
		return str("Device ID = "+self.deviceID +" 		Reader IP = "+self.readerIP)
