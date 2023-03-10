from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    point1 = models.IntegerField(null=True)
    point2 = models.IntegerField(null=True)
    point3 = models.IntegerField(null=True)
    token = models.IntegerField(null=True)

    def __str__(self):
        return self.name

class Categories(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name
    
class Brand(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=200, null=True)
    code = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Filter_Price(models.Model):

    FILTER_PRICE = (
        ('')
    )

    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return self.price
    


class Product(models.Model):
    STOCK = ('IN STOCK','IN STOCK'),('OUT OF STOCK','OUT OF STOCK')

    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(blank=True, null=True, upload_to = 'images/')
    description = models.TextField(null=True, blank=True)
    stock = models.CharField(choices=STOCK, max_length=200,null=True)

    categories = models.ForeignKey(Categories,on_delete=models.CASCADE,null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE,null=True, blank=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE,null=True, blank=True)
    filter_price = models.ForeignKey(Filter_Price, on_delete=models.CASCADE,null=True, blank=True)

    
    def __str__(self):
        return self.name

    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum ([ item.get_total for item in orderitems]) 
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum ([ item.quantity for item in orderitems]) 
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAdress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

class Carousel(models.Model):
    title = models.CharField(max_length=200, null=True)
    sub_title = models.CharField(max_length=200, null=True)
    image = models.ImageField(blank=True, null=True, upload_to = 'images/')
    
    def __str__(self):
        return self.title

    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
# class ImagePathField(models.CharField):
#     def _init_(self, *args, **kwargs):
#         self.upload_to = kwargs.pop('upload_to', None)
#         super(ImagePathField, self)._init_(*args, **kwargs)

#     def pre_save(self, model_instance, add):
#         file = getattr(model_instance, self.attname)
#         if file:
#             filename = os.path.join(settings.MEDIA_ROOT, self.upload_to, file.name)
#             file_path = os.path.join(self.upload_to, file.name)
#             if not os.path.exists(filename):
#                 with open(filename, 'wb+') as destination:
#                     for chunk in file.chunks():
#                         destination.write(chunk)
#             setattr(model_instance, self.attname, file_path)
#         return super(ImagePathField, self).pre_save(model_instance, add)