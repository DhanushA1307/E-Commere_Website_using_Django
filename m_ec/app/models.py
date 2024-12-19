from django.db import models
from django.contrib.auth.models import User

STATE_CHOICES = (
("Andhra Pradesh","Amaravati"),
("Arunachal Pradesh","Itanagar"),
("Assam","Dispur"),
("Bihar","Patna"),
("Chhattisgarh","Raipur"),
("Goa","Panaji"),
("Gujarat","Gandhinagar"),
("Haryana","Chandigarh"),
("Himachal Pradesh","Shimla"),
("Jharkhand","Ranchi"),
("Karnataka","Bengaluru"),
("Kerala","Thiruvananthapuram"),
("Madhya Pradesh","Bhopal"),
("Maharashtra","Mumbai"),
("Manipur","Imphal"),
("Meghalaya","Shillong"),
("Mizoram","Aizawl"),
("Nagaland","Kohima"),
("Odisha","Bhubaneswar"),
("Punjab","Chandigarh"),
("Rajasthan","Jaipur"),
("Sikkim","Gangtok"),
("Tamil Nadu","Chennai"),
("Telangana","Hyderabad"),
("Tripura","Agartala"),
("Uttar Pradesh","Lucknow"),
("Uttarakhand","Dehradun"),
("West Bengal","Kolkata")
)

CATEGORY_CHOICES =(
    ('SH', 'Shirt'),
    ('PT', 'Pant'),
    ('DE', 'Denim'),
    ('JS', 'Jeans'),
    ('RG', 'Ring'),
    ('PF', 'Perfume'),
    ('WT', 'Watch'),
    ('BL', 'Belt'),
    ('CH', 'Chain'),
    ('SK', 'Socks')
)

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discount_price = models.FloatField()
    description = models.TextField()
    composition = models.TextField(default='')
    prodapp = models.TextField(default='')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='product')
    
    def __str__(self):
        return self.title
    
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.IntegerField(default=0)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=100)
    
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity*self.product.discount_price
    

STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('Packed', 'Packed'),
    ('On The Way','On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
    ('Pending','Pending')
)

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    paid = models.BooleanField(default=True)
    
'''
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_status = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    paid = models.BooleanField(default=False)
'''


class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    payment = models.ForeignKey(Payment,on_delete=models.CASCADE,default="")
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='Pending')
    @property
    def total_cost(self):
        return self.quantity * self.product.discount_price

'''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Delivered', 'Delivered')], default='Pending')
 '''   
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)