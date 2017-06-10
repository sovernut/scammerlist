from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class Catalog(models.Model):
    type_cat = models.CharField(max_length=200)

    def __str__(self):
        return self.type_cat

class Person(models.Model):
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    mobile_number = models.CharField(max_length=10)
    detail = models.CharField(max_length=400)
    picture_url = models.CharField(max_length=100,default="https://assets.pcmag.com/media/images/357201-how-to-lock-down-your-facebook-profile.jpg?thumb=y&width=275&height=275")
    last_report_time = models.DateTimeField(timezone.now())
    
    def __str__(self):
        return self.name
        
class Report(models.Model):
    reporter_name = models.OneToOneField(User,null=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    report_detail = models.CharField(max_length=400)
    report_time = models.DateTimeField(timezone.now())
    
    def __str__(self):
        return self.report_detail
