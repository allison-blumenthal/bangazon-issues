from django.db import models
from .user import User
from .payment import Payment

class Order(models.Model):
  
  customer_id = models.ForeignKey(User, on_delete=models.CASCADE)
  payment_id = models.ForeignKey(Payment, on_delete=models.CASCADE)
  total = models.DecimalField(max_digits=6, decimal_places=2)
  needs_shipping = models.BooleanField()
  is_completed = models.BooleanField()
  date_placed = models.DateField()
  
  
