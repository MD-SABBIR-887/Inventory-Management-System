from rest_framework import serializers
from . import models

class CutomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = '__all__'
        
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,min_length=6)
    class Meta:
        model = models.CustomUser
        fields = ['username','email','password','first_name','last_name',]

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = models.CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def updated(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
            instance.save()
        return instance
    
class UserProfileSerializer(serializers.ModelSerializer):
    class meta:
        model = models.UserProfile
        fields = ['id','user','phone','address','city',]
        
    def validate_phone(self, value):
        if value and len(value) < 11:
            raise serializers.ValidationError("Phone number must contain at least 10 characters.")
        return value
        
class CustomerCategorySerializer(serializers.ModelSerializer):
    class meta:
        model = models.CustomerCategory
        fields = '__all__'
        
class CustomerSerializer(serializers.ModelSerializer):
    class meta:
        model = models.Customer
        fields = ['id','name','email','phone','address','category','created_at',]
        def validate_phone(self, value):
            if len(value) < 11:
                raise serializers.ValidationError("Invalid phone number.")
            return value
        
class ProductSerializer(serializers.ModelSerializer):
    class meta:
        model = models.Product
        fields = '__all__'
        
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value
        
class InvoiceSerializer(serializers.ModelSerializer):
    class meta:
        model = models.Invoice
        fields = ['id','customer','product','quantity','price','total_price','created_by','created_at',]

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0.")
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value

    def validate(self, attrs):
        product = attrs.get('product')
        quantity = attrs.get('quantity')

        if product and quantity:
            if product.stock < quantity:
                raise serializers.ValidationError({'quantity': 'Not enough product stock available.'})
        return attrs

    def create(self, validated_data):
        product = validated_data['product']
        quantity = validated_data['quantity']
        price = validated_data['price']
        total = quantity * price
        invoice = models.Invoice.objects.create(total=total,**validated_data)
        product.stock -= quantity
        product.save()

        return invoice