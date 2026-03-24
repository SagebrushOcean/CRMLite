from rest_framework import serializers
from .models import Company, Storage#, Supplier, Supply, Product

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"

class StorageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    company_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Storage
        fields = ['id', 'address', 'company_id']

# class SupplierSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(read_only=True)
#     company_id = serializers.PrimaryKeyRelatedField(read_only=True)
#
#     class Meta:
#         model = Supplier
#         fields = ['id','INN', 'title', 'company_id']
#
# class SupplySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Supply
#         fields = "__all__"
#
# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ['id','title','description', 'quantity','purchase_price','sale_price','created_at','updated_at','storage_id']

