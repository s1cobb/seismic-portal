# system defined module
from rest_framework import serializers

# user defined table models
from customer.models import StoreInfo
from customer.models import StaffInfo
from customer.models import RentalInfo
from customer.models import AddressInfo
from customer.models import CustomerInfo
from customer.models import InventoryInfo

#  serializer classes
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
       model = CustomerInfo
       fields = '__all__'
       extra_kwargs = {'customer_id': {'required': False}, 'store_id': {'required': False},
                       'first_name': {'required': False}, 'last_name': {'required': False},
                       'email': {'required': False}, 'address_id': {'required': False}, 
                       'activebool': {'required': False}, 'create_date': {'required': False},
                       'last_update': {'required': False}, 'active': {'required': False}}
                
class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentalInfo
        fields = '__all__'
        extra_kwargs = {'rental_id': {'required': False}, 'rental_date': {'required': False},
                        'inventory_id': {'required': False}, 'customer_id': {'required': False},
                        'return_date': {'required': False}, 'staff_id': {'required': False},
                        'last_update': {'required': False}}

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
       model = StoreInfo
       fields = '__all__'
       extra_kwargs = {'store_id': {'required': False}, 'manager_staff_id': {'required': False},
                       'address_id': {'required': False}, 'last_update': {'required': False}}

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
       model = InventoryInfo
       fields = '__all__'
       extra_kwargs = {'inventory_id': {'required': False}, 'film_id': {'required': False},
                       'store_id': {'required': False}, 'last_update': {'required': False}}

       
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressInfo
        fields = '__all__'
        extra_kwargs = {'address_id': {'required': False}, 'address': {'required': False},
                       'address2': {'required': False}, 'district': {'required': False}, 
                       'city_id': {'required': False}, 'postal_code': {'required': False}, 
                       'phone': {'required': False}, 'last_update': {'required': False}}
                 
class StaffSerializer(serializers.ModelSerializer):
    model = StaffInfo
    fields = '__all__'
    extra_kwargs = {'staff_id': {'required': False}, 'first_name': {'required': False},
                    'last_name': {'required': False}, 'address_id': {'required': False},
                    'email': {'required': False}, 'store_id': {'required': False},
                    'active': {'required': False}, 'username': {'required': False}, 
                    'password': {'required': False}, 'last_update': {'required': False},
                    'picture': {'required': False}}
        