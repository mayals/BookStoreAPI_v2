from django.shortcuts import render
from .serializers import CategorySerializer,BookSerializer,PublisherSerializer
from rest_framework import viewsets
from .models import Category, Book, Publisher, Author, Review, UserModel, Order, Ordering, Cart
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser


# https://www.django-rest-framework.org/api-guide/status-codes/#successful-2xx
# https://www.django-rest-framework.org/api-guide/parsers/#parsers
# https://stackoverflow.com/questions/57689088/what-are-the-parsers-used-for-in-the-django-rest-framework




class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    lookup_field = 'slug' 






class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'                 # must write this to  make slug as lookup_field

    # https://stackoverflow.com/questions/57689088/what-are-the-parsers-used-for-in-the-django-rest-framework
    parser_classes = [FormParser, MultiPartParser, JSONParser]   #https://www.django-rest-framework.org/api-guide/parsers/#parsers


    # work ok 
    # @action(detail=True,methods= ['put'])
    # def update_category(self, request,*args,**kwargs):
    #     slug = kwargs.get('slug')
    #     category = get_object_or_404(Category, slug=slug)
    #     serializer = CategorySerializer(category, data= request.data, partial= partial, context = {'request': request})
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status = status.HTTP_200_OK)
    #     else:
    #         return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        
        
    def update(self, request,*args,**kwargs):
        slug = kwargs.get('slug')
        category = get_object_or_404(Category, slug=slug)
        serializer = CategorySerializer(category, data= request.data, partial= partial, context = {'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)   
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)



    # https://www.youtube.com/c/AaravTech
    # work ok 
        # @action(detail=True,methods= ['put'])
        # def update_category(self, request,*args,**kwargs):
        #     slug = kwargs.get('slug')
        #     category = get_object_or_404(Category, slug=slug)
        #     serializer = CategorySerializer(category, data= request.data, partial= partial, context = {'request': request})
        #     if serializer.is_valid():
        #         serializer.save()
        #         return Response(serializer.data, status = status.HTTP_200_OK)
        #     else:
        #         return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


    
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer 
    lookup_field = 'slug'  





# def update(self, request, *args, **kwargs):
    #     partial = True # Here I change partial to True
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)

    #     return Response(serializer.data, status = status.HTTP_200_OK)
 