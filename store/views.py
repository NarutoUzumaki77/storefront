from typing import Collection
from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer


@api_view(['GET', 'POST'])
def products(request):
    if request.method == 'GET':
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if product.orderitem_set.count() > 0:
            return Response(
                {'error': 'Product cannot be deleted because it is associated to an OrderItem.'})
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def collections_list(request):
    if request.method == 'GET':
        queryset = Collection.objects.annotate(
            products_count=Count('product')).all()
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def collection_details(request, id):
    collection = get_object_or_404(Collection.objects.annotate(
        products_count=Count('product')), pk=id)
    if request.method == 'GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if collection.product_set.count() > 0:
            return Response(
                {'error': 'Collection can not be deleted because it include one or more products.'})
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
