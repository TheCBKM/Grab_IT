from django.db import models
from django.contrib.auth.models import User
from PIL import Image 
from io import BytesIO
import datetime




















from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


# Create your models here.

class Seller(models.Model):
    user = models.ForeignKey( User,on_delete=models.CASCADE)
    branch = models.CharField(max_length=20,default='')
    contact = models.IntegerField(default=0)
    lcount = models.IntegerField(default=0)
    isadmin = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username + '/'+ str(self.id)


class Category(models.Model):
    name = models.CharField(max_length=20, default='',unique=True)
    count = models.IntegerField(default=0)
    image = models.ImageField(upload_to='shop/catimages',default='', blank=True, null=True)

    def __str__(self):
        return self.name + '/'+ str(self.id)

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, default='', unique=True)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.name + '/'+ str(self.id)

class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, default='')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, default='')
    price = models.IntegerField(default=100)
    status = models.IntegerField(default=0)
    contact = models.IntegerField(default=0)
    image = models.ImageField(upload_to='shop/images',default='')
    # 0 => not approved
    # 1 => approved
    # 2 => sold
    # 3 => category not exist
    # 4 => subcategory not exist
    # 5 => product not exist

    def save(self, *args, **kwargs):
        imageTemproary = Image.open(self.image)
        outputIoStream = BytesIO()
        # imageTemproaryResized = imageTemproary.resize( (900,300) ) 
        imageTemproary.save(outputIoStream , format='JPEG', quality=10)
        outputIoStream.seek(0)
        self.image = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" %self.image.name.split('.')[0], 'image/jpeg/png', sys.getsizeof(outputIoStream), None)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name + '/'+ str(self.id)

class Request(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default='')
    name = models.CharField(max_length=20, default='')
    contact = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)

    

class Pcount(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self):
        return str(self.count)




   # Grab_IT1565642939041                                                                                