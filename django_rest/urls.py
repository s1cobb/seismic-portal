# customer info urls

from customer import views
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
               path('v1/customers', views.CustomerList.as_view()),
               path('v1/customer/<int:id>', views.SingleCustomer.as_view()),
               path('v1/rentals', views.RentalList.as_view()),
               path('v1/rental/<int:id>', views.SingleRental.as_view()),
               path('v1/stores', views.StoreList.as_view()),
               path('v1/store/<int:id>', views.SingleStore.as_view())
              ]
              
urlpatterns = format_suffix_patterns(urlpatterns)