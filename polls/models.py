from django.db import models

# Create your models here.
class Poll(models.Model):
	question = models.CharField(max_length=200)
	pub_date = models.DateTimeField(verbose_name='Date published')

	def __str__(self):
		return self.question

class Choice(models.Model):
	poll = models.ForeignKey(Poll)
	choice = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)