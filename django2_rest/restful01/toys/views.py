from toys.models import Toys


from rest_framework import status
from django.shortcuts import render
from toys.serializers import ToySerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view


# Create your views here.

@api_view(['GET', 'POST'])
def toy_list(request):
    if request.method == 'GET':
        toys = Toys.objects.all()
        toy_serial = ToySerializer(toys, many=True)
        return Response(toy_serial.data)
    elif request.method == 'POST':
        toy_serial = ToySerializer(data=request.data)
        if toy_serial.is_valid():
            toy_serial.save()
            return Response(toy_serial.data, status=status.HTTP_201_CREATED)
        return Response(toy_serial.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'GET', 'DELETE'])
def toy_detail(request, pk):
    try:
        toy = Toys.objects.get(pk=pk)
    except Toys.DoesNotExist:
        return Response(status=status.HTTP_404_BAD_REQUEST)

    if request.method == 'GET':
        toy_serial = ToySerializer(toy)
        return Response(toy_serial.data)
    elif request.method == 'PUT':
        toy_serial = ToySerializer(toy, data=request.data)
        if toy_serial.is_valid():
            toy_serial.save()
            return Response(toy_serial.data)
        return Response(toy_serial.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        toy.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




