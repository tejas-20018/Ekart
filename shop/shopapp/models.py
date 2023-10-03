from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Product(models.Model):
    CAT=(('1','metal'),('2','electronics'))
    name=models.CharField(max_length=50,verbose_name="product name")
    price=models.FloatField()
    cat=models.CharField(max_length=10,verbose_name='category',choices=CAT)
    is_active=models.BooleanField(default=1)
    pimage=models.ImageField(upload_to='image')

    def __str__(self):
        return self.name

class Cart(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')
    pid=models.ForeignKey(Product,on_delete=models.CASCADE,db_column='pid')
    qty=models.IntegerField(default=1)

class Orders(models.Model):
    order_id=models.IntegerField()
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')
    pid=models.ForeignKey(Product,on_delete=models.CASCADE,db_column='pid')
    qty=models.IntegerField(default=1)



