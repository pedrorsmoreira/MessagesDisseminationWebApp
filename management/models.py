from django.db import models
from django.utils import timezone

# Create your models here.


class Buildings(models.Model):
	id = models.CharField(max_length = 255, primary_key = True)
	name = models.CharField(max_length = 255)
	lat = models.FloatField()
	longit= models.FloatField()

	def __str__(self):
		return self.id

class Users(models.Model):
	ist_id = models.CharField(max_length = 10, primary_key = True)
	name = models.CharField(max_length = 255)
	build_id = models.CharField(max_length = 255)
	range_user = models.IntegerField()
	lat = models.FloatField()
	longit = models.FloatField()

	def __str__(self):
		return self.ist_id


class Messages(models.Model):
	content = models.CharField(max_length = 255)
	receiver = models.ForeignKey(Users, on_delete = models.CASCADE)
	date = models.DateTimeField(default = timezone.now)

	def __str__(self):
		return self.content