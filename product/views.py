from django.shortcuts import render
from product.models import Catagory, Product
from .serializers import FileUploadSerializer, ProductSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# from django_filters.rest_framework import DjangoFilterBackend
import csv
import io



class DemoView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({'success':'you are authenticated'})


class ProductView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request, pk = None):
        catagory = self.request.query_params.get('catagory')
        if pk is not None:
            stu = Product.objects.get(id =pk)
            serializer = ProductSerializer(stu)
            return Response(serializer.data)
        
        elif catagory:
            queryset = Product.objects.filter(catagory__catagory_name = catagory)
        
        else:
            queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many = True)
        return Response({'count':len(serializer.data) ,'data':serializer.data})

    def post(self, request):
        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid():
            catagory = serializer.validated_data['catagory']
            product_name = serializer.validated_data['product_name']
            price = serializer.validated_data['price']
            product = Product.objects.create(catagory  = catagory, product_name = product_name, price = price)
            product.save()
            serializer.save()
        return Response({'msg':'Your Product has been added successfully'})
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['catagory']


class AddProductCsv(APIView):
    def post(self, request):
        serializer = FileUploadSerializer(data = request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            decoded_file = file.read().decode()
            io_string = io.StringIO(decoded_file)
            reader = csv.reader(io_string)
            for i in reader:
                print(i)
                catagory = Catagory.objects.get(catagory_name = i[0])    
                Product.objects.create(catagory = catagory, product_name = i[1], price = i[2])
            return Response({'msg':'Products has been added!'})
                