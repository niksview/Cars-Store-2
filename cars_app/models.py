from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    CAT=((1,'Parts'),(2,'Sizes'),(3,'Colours'),(4,'Assesories'))
    name=models.CharField(max_length=50, verbose_name="Part Name")
    price=models.FloatField()
    pdetails=models.CharField(max_length=100, verbose_name="Part Details")
    cat=models.IntegerField(choices=CAT,verbose_name="Category")
    is_active=models.BooleanField(default=True,verbose_name="Available")
    pimage=models.ImageField(upload_to='image')

class Cart(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE, db_column="uid")
    pid=models.ForeignKey(Product,on_delete=models.CASCADE,db_column="pid")
    qty=models.IntegerField(default=1)

class Order(models.Model):
    order_id=models.CharField(max_length=50)
    uid=models.ForeignKey(User,on_delete=models.CASCADE, db_column="uid")
    pid=models.ForeignKey(Product,on_delete=models.CASCADE,db_column="pid")
    qty=models.IntegerField(default=1)
