from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Cart, CartItem, Order, OrderItem
from .serializers import CartItemCreateSerializer, CartItemSerializer,CartSerializer, OrderItemSerializer, OrderSerializer

# Create your views here.

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def manage_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    serializer = CartSerializer(cart)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    serializer = CartItemCreateSerializer(data=request.data)

    if serializer.is_valid():
        product = serializer.validated_data['product']
        quantity = serializer.validated_data.get('quantity', 1)

        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart, product=product,
            defaults={'quantity': quantity}
        )
        if not item_created:
            cart_item.quantity += quantity
            if product.stock < cart_item.quantity:
                return Response({"error": "Exceeds available stock."}, status=status.HTTP_400_BAD_REQUEST)
            cart_item.save()
        return Response(CartItemSerializer(cart_item).data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart_items(request):
    items = CartItem.objects.filter(cart__user=request.user)
    serializer = CartSerializer(items, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_order(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)
    if not cart_items.exists():
        return Response ({"error": "cart is empty."}, status=status.HTTP_400_BAD_REQUEST)
    
    total = 0
    for item in cart_items:
        if item.product.stock < item.quantity:
            return Response({"error": f"insufficient stock for {item.product.name}."}, status=status.HTTP_400_BAD_REQUEST)
        total += item.product.price * item.quantity

    with transaction.atomic():
        order = Order.objects.create(user=request.user, total_price=total)
        for item in cart_items:
            product = item.product
            product.stock -= item.quantity
            product.save()

            OrderItem.objects.create(order=order, product=product, quantity=item.quantity)
        
        cart_items.delete()

    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders(request):
    orders = Order.objects.filter(user=request.user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)