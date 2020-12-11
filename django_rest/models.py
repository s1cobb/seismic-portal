from django.db import models

# Create your models here.
class AddressInfo(models.Model):
   address_id = models.IntegerField(primary_key=True)
   address = models.CharField(max_length=50)
   address2 = models.CharField(max_length=50, blank=True)
   district = models.CharField(max_length=20)
   city_id = models.SmallIntegerField()
   postal_code = models.CharField(max_length=10, blank=True)
   phone = models.CharField(max_length=20)
   last_update = models.DateTimeField(auto_now_add=True)

class InventoryInfo(models.Model):
   inventory_id = models.IntegerField()
   film_id = models.SmallIntegerField()
   store_id = models.SmallIntegerField()
   last_update = models.DateTimeField(auto_now_add=True)
   
class StaffInfo(models.Model):
   staff_id = models.IntegerField(primary_key=True)
   first_name = models.CharField(max_length=45)
   last_name = models.CharField(max_length=45)
   address_id = models.SmallIntegerField()
   email = models.CharField(max_length=50, blank=True)
   store_id = models.SmallIntegerField()
   active = models.BooleanField(default='t')
   username = models.CharField(max_length=16)
   password = models.CharField(max_length=40, blank=True)
   last_update = models.DateTimeField(auto_now_add=True)
   
class CustomerInfo(models.Model):
   customer_id = models.IntegerField(primary_key=True)
   store_id = models.SmallIntegerField()
   first_name = models.CharField(max_length=45)
   last_name = models.CharField(max_length=45)
   email = models.CharField(max_length=50, blank=True)
   address_id = models.SmallIntegerField()
   activebool = models.BooleanField(default='t')
   create_date = models.DateField()
   last_update = models.DateTimeField(auto_now_add=True)
   active = models.IntegerField()
   
class RentalInfo(models.Model):
   rental_id = models.IntegerField(primary_key=True)
   rental_date = models.DateTimeField(auto_now_add=True)
   inventory_id = models.IntegerField()
   customer_id = models.SmallIntegerField()
   return_date = models.DateTimeField(auto_now_add=True, blank=True)
   staff_id = models.SmallIntegerField()
   last_update = models.DateTimeField(auto_now_add=True)
   
class StoreInfo(models.Model):
   store_id = models.IntegerField(primary_key=True)
   manager_staff_id = models.SmallIntegerField()
   address_id = models.SmallIntegerField()
   last_update = models.DateTimeField(auto_now_add=True)