from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.


# class Profiel(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     profile_pic = models.ImageField(null=True, blank=True)



# fuel/petrol type table.
class Fuel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.FloatField(max_length=(15,2), default=0)
    user = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=2,choices=(('1','Active'),('0', 'Inactive')) , default = 1)
    delete_flag = models.IntegerField(default = 0)
    created = models.DateTimeField(default = timezone.now)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated','-created']
        verbose_name_plural = "fuel type lists"

    def __str__(self):
        return self.name



    
    # returns the available volume for each fuel. subtracting the volume in sale from the volume in 
    def available(self):
        try:
            stockin = Stock.objects.filter(fuel = self).aggregate(models.Sum("volume"))['volume__sum']
            if stockin is None:
                stockin = 0
        except:
            stockin = 0
        try:
            sale = Sale.objects.filter(fuel = self).aggregate(models.Sum("volume"))['volume__sum']
            if sale is None:
                sale = 0
        except:
            sale = 0
            print(sale)
        return stockin - sale

# stock manager table.
class Stock(models.Model):
    date = models.DateField(null=True, blank = True)
    fuel = models.ForeignKey(Fuel, on_delete=models.CASCADE)
    volume = models.FloatField(max_length=(15,2),default=0)
    user = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated','-created']
        verbose_name_plural = "Stock lists"

    def __str__(self):
        return f"{self.fuel.name} - [{self.volume} L]"


# sales model/table
class Sale(models.Model):
    customer_name = models.CharField(max_length=200)
    fuel = models.ForeignKey(Fuel, on_delete=models.CASCADE)
    volume = models.FloatField(max_length=(15,2), default=0)
    amount = models.FloatField(max_length=(15,2), default=0)
    user = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Sales list"
        ordering = ['-updated', '-created']
    

    def __str__(self):
        return f"{self.customer_name} - [{self.fuel} - {self.volume} L]"
    
    

