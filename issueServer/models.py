from django.db import models
class device_info(models.Model):
	device_id = models.CharField(max_length=20)
	device_ip = models.GenericIPAddressField(default=None)
	def __str__(self):
		return str(self.device_id)
	def __unicode__(self):
		return str(self.device_id)

