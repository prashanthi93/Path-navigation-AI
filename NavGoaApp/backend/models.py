from django.db import models
from datetime import datetime
# Create your models here.

class Paths(models.Model):
    source = models.CharField(max_length=200,null=False,blank=False)
    destination = models.CharField(max_length=200,null=False,blank=False)
    path = models.JSONField(null = True,blank=True)
    heuristicCost = models.IntegerField()
    travelTime = models.IntegerField()
    created = models.DateTimeField(auto_now=True)
    hour = models.IntegerField(null=True, blank=True)
    minute = models.IntegerField(null=True, blank=True)
    count = 0
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.created and not self.count:
            self.hour = self.created.hour
            self.minute = self.created.minute
            self.count += 1
            self.save()
        else:
            return
    def __str__(self):
        return "Path ({} -> {}) at {}hr {}min".format(self.source,self.destination,self.hour,self.minute)