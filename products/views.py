from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from products.models import Product, ProductSpecifications
from products.serializers import ProductSerializer, ProductSpecificationsSerializer
from decimal import Decimal, ROUND_UP


@api_view(['GET', 'POST'])
def products_list(request):
    """
    List all code products, or create a new products.
    """
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        processed_data = request.data
        processed_data['user'] = str(request.user.id)
        price = Decimal(processed_data['price']).quantize(Decimal('.01'), rounding=ROUND_UP)

        if processed_data.get("calc_percentage", False):
            processed_data['price'] = Decimal(price + price*Decimal(0.3)).quantize(Decimal('.01'), rounding=ROUND_UP)

        serializer = ProductSerializer(data=processed_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def products_detail(request, pk):
    """
    Retrieve, update or delete a code products.
    """
    try:
        products = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductSerializer(products)
        return Response(serializer.data)

    elif request.method == 'PUT':
        processed_data = request.data
        price = Decimal(processed_data['price']).quantize(Decimal('.01'), rounding=ROUND_UP)
        if processed_data["calc_percentage"] == 'true':
            processed_data['price'] = Decimal(price + price*Decimal(0.3)).quantize(Decimal('.01'), rounding=ROUND_UP)

        serializer = ProductSerializer(products, data=processed_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        products.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT', 'DELETE'])
def product_specification(request, specification_id):
    try:
        specification_product = ProductSpecifications.objects.get(pk=specification_id)
    except ProductSpecifications.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ProductSpecificationsSerializer(specification_product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        specification_product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
