from rest_framework import serializers
from .models import Company, Storage, Supplier, Supply, Product, SupplyProduct

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

class SupplierSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    company_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Supplier
        fields = ['id','INN', 'title', 'company_id']

class CreateSupplyProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=False)
    quantity = serializers.IntegerField(max_value=1000, min_value=0)

    class Meta:
        model = Product
        fields = ['id','quantity']

class CreateSupplySerializer(serializers.ModelSerializer):
    products = CreateSupplyProductSerializer(many=True)

    class Meta:
        model = Supply
        fields = ['supplier_id', 'delivery_date', 'products']

class ListSupplyProductSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(read_only=True)
    quantity = serializers.IntegerField()

    class Meta:
        model = SupplyProduct
        fields = ['product_id','quantity']

class ListSupplySerializer(serializers.ModelSerializer):
    supply_products = ListSupplyProductSerializer(many=True)

    class Meta:
        model = Supply
        fields = ['id','supplier_id', 'delivery_date', 'supply_products']

class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title','description','purchase_price','sale_price']

class ProductSerializer(ProductUpdateSerializer):
    class Meta(ProductUpdateSerializer.Meta):
        fields = ['id'] + ProductUpdateSerializer.Meta.fields + ['quantity','storage_id', 'created_at','updated_at']



