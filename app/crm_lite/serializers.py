from rest_framework import serializers
from .models import Company, Storage # Product

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"

class StorageSerializer(serializers.ModelSerializer):
    company_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Storage
        fields = ['address', 'company_id']

# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = "__all__"




