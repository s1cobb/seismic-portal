# system defined modules
from django.http import Http404
from rest_framework import status
from rest_framework import filters
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

# user defined modules
from customer.models import StoreInfo
from customer.models import StaffInfo
from customer.models import RentalInfo
from customer.models import AddressInfo
from customer.models import CustomerInfo

# user defined serializers
from customer.serializers import StaffSerializer
from customer.serializers import StoreSerializer
from customer.serializers import RentalSerializer
from customer.serializers import AddressSerializer
from customer.serializers import CustomerSerializer
from customer.serializers import InventorySerializer


################################################################
#
# Customer table
################################################################
class CustomerList(generics.ListAPIView):
    ''' 
       List all Customers or create new custoner
    '''
    
    # query table data 
    queryset = CustomerInfo.objects.all()
    
    serializer_class = CustomerSerializer
    
    # set filters per view
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['active', 'first_name', 'last_name', 'email', 'address_id']
    
#############################################################
#    
# Customer table, single record interaction
#############################################################
class SingleCustomer(APIView):
    ''' This class interacts with individual table records. '''
    
    # get customer object or return error
    def get_object(self, id):
       try:
          return CustomerInfo.objects.get(customer_id=id)
       except CustomerInfo.DoesNotExist:
          raise Http404
       
    # get individual customer record
    def get(self, request, id, format=None):
        cust = self.get_object(id)
        serial = CustomerSerializer(cust)
        return Response(serial.data)
        
    def post(self, request, id, format=None):
        serial = CustomerSerializer(data=request.data)
        
        if serial.is_valid():
            serial.save()
            return Response(serial.data, status=status.HTTP_201_CREATED)
        return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # update a individual record    
    def put(self, request, id, format=None):
        cust = self.get_object(id)

        serial = CustomerSerializer(cust, data=request.data)       
        if serial.is_valid():
           serial.save()
           return Response(serial.data, status=status.HTTP_201.CREATED)
        return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # remove from record.     
    def delete(self, request, id, format=None):
        cust = self.get_object(id)
        cust.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

####################################################################
#
# Rental table single record interaction
####################################################################        
class RentalList(generics.ListAPIView):
    ''' 
       List all rentals or create rental
    '''
    
    # query table data 
    queryset = RentalInfo.objects.all()
    
    serializer_class = RentalSerializer
    
    # set filters per view
    filter_backends = [DjangoFilterBackend]
    
    # gives the ability to search on these fields in the url
    filterset_fields = ['rental_id', 'inventory_id', 'customer_id', 'staff_id']
        
        
class SingleRental(APIView):
    ''' This class interacts with the Rental table. '''
    
    # get rental record or error
    def get_object(self, id):
        try:
            return RentalInfo.objects.get(rental_id=id)
        except RentalInfo.DoesNotExist:
            raise Http404
    
    # get rental record from table    
    def get(self, request, id, format=None):
        rec = self.get_object(id)
        serial = RentalSerializer(rec)
        return Response(serial.data)
    
    # create a new entry    
    def post(self, request, id, format=None):
        print(request.data)
        serial = RentalSerializer(data=request.data)
        
        if serial.is_valid():
           serial.save()
           return Response(serial.data, status=status.HTTP_201_CREATED)
        return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
        
    # update the rental record
    def put(self, request, id, format=None):
        rec = self.get_object(id)
        
        serial = RentalSerializer(rec, data=request.data)
        if serial.is_valid():
            serial.save()
            return Response(serial.data, status=status.HTTP_201_CREATED)
        return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # remove rental record.    
    def delete(self, request, id, format=None):
        rec = self.get_object(id)
        rec.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#### will refactor later        
class StoreList(generics.ListAPIView):
    ''' 
       List all stores or create new store
    '''       
    # query table data 
    queryset = StoreInfo.objects.all()
    
    serializer_class = StoreSerializer
    
    # set filters per view
    filter_backends = [DjangoFilterBackend]
    
    # gives the ability to search on these fields in the url
    filterset_fields = ['store_id', 'manager_staff_id', 'address_id']
                

# Single store record details
class SingleStore(APIView):
    ''' This class interacts with Store records. '''
    
    # return store record or error
    def get_object(self, id):
        try:
            return StoreInfo.objects.get(store_id=id)
        except StoreInfo.DoesNotExist:
            raise Http404
    
    # get store record from table    
    def get(self, request, id, format=None):
        stor = self.get_object(id)
        serial = StoreSerializer(stor)
        return Response(serial.data)
        
    def post(self, request, id, format=None):
        serial = StoreSerializer(data=request.data)
        
        if serial.is_valid():
            serial.save()
            return Response(serial.data, status=status.HTTP_201_CREATED)
        return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)

    # update the store record
    def put(self, request, id, format=None):
        rec = self.get_object(id)
        
        serial = StoreSerializer(rec, data=request.data)
        if serial.is_valid():
            serial.save()
            return Response(serial.data, status=status.HTTP_201_CREATED)
        return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST) 

    def delete(self, request, id, format=None):
        rec = self.get_object(id)
        rec.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)