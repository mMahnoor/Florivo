from django.shortcuts import render
from rest_framework import viewsets
from orders import serializers as order_serializers
from orders.models import Order, OrderItem
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from orders.services import OrderService
from rest_framework.response import Response

# Create your views here.
class OrderViewset(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'delete', 'patch', 'head', 'options']

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        OrderService.cancel_order(order=order, user=request.user)
        return Response({'status': 'Order cancelled'})

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        serializer = order_serializers.UpdateOrderSerializer(
            order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status": f"Order status updated to {request.data['status']}"})

    def get_permissions(self):
        if self.action in ['update_status', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'cancel':
            return order_serializers.EmptySerializer
        if self.action == 'create':
            return order_serializers.CreateOrderSerializer
        elif self.action == 'update_status':
            return order_serializers.UpdateOrderSerializer
        return order_serializers.OrderSerializer

    def get_serializer_context(self):
        # if getattr(self, 'swagger_fake_view', False):
        #     return super().get_serializer_context()
        return {'user_id': self.request.user.id, 'user': self.request.user}

    def get_queryset(self):
        # if getattr(self, 'swagger_fake_view', False):
        #     return Order.objects.none()
        if self.request.user.is_staff:
            return Order.objects.prefetch_related('items__flower').all()
        return Order.objects.prefetch_related('items__flower').filter(user=self.request.user)