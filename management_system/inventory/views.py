from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate
from django.db.models import Sum, Count
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from .models import (CustomUser,UserProfile,CustomerCategory,Customer,Product,Invoice)
from .serializer import (CutomUserSerializer,UserRegistrationSerializer,UserProfileSerializer,CustomerCategorySerializer,CustomerSerializer,ProductSerializer,InvoiceSerializer)
from .permissions import (IsAdmin,IsUsers)


class RegisterView(APIView):
    permission_classes = [AllowAny]
    # def get(self, request):
    #     users = CustomUser.objects.filter()
    #     serializer = CutomUserSerializer(users, many=True)
    #     return Response(serializer.data)
    
    def post (self, request):
        serializer = UserRegistrationSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response (serializer.data, status=status.HTTP_201_CREATED)
        
        
class ProfileView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin, IsUsers]
    def get_object(self, pk, request):
        try:
            return UserProfile.objects.get(pk=pk)
        except UserProfile.DoesNotExist:
            return None
        
    def get(self, request, pk):
        user = self.get_object(pk, request)
        if not user:    
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(UserProfileSerializer(user).data)
        
    def put(self, request, pk):
        user = self.get_object(pk, request)
        if not user:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserProfileSerializer(user,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
            
    def patch(self, request, pk):
        user = self.get_object(pk, request)
        if not user:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserProfileSerializer(user,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, pk):
        user = self.get_object(pk)
        if not user:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CustomerCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdmin, IsUsers]
    queryset = CustomerCategory.objects.all()
    serializer_class = CustomerCategorySerializer
    
class CustomerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdmin, IsUsers]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    
class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdmin, IsUsers]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.select_related('customer','product','created_by').all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAdmin, IsUsers]
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        
class InvoiceReportView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        total_invoices = Invoice.objects.count()
        total_sales = Invoice.objects.aggregate(total=Sum('total'))['total'] or 0
        total_products_sold = Invoice.objects.aggregate(total=Sum('quantity'))['total'] or 0
        return Response({
            'total_invoices': total_invoices,
            'total_sales': total_sales,
            'total_products_sold': total_products_sold,
        })
    