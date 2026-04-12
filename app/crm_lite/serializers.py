from django.utils import timezone
from rest_framework import serializers
from .models import Company, Storage, Supplier, Supply, Product, SupplyProduct, Sale

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

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

class SaleSerializer(serializers.ModelSerializer):
    product_sales = CreateSupplyProductSerializer(many=True, write_only=True)

    class Meta:
        model = Sale
        read_only_fields = ['id', 'sale_date']
        fields = ['id','buyer_name','product_sales','sale_date']

class UpdateSaleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sale
        fields = ['id','buyer_name','sale_date']

    def validate_sale_date(self, value):
        if value > timezone.now():
            raise serializers.ValidationError('Дата продажи не должна превышать текущую')
        return value

class HealthCheckSerializer(serializers.Serializer):
    DATABASE = 0
    API_INTEGRATION = 1

    COMPONENT_CHOICES = [
        (DATABASE, "Database"),
        (API_INTEGRATION, "API Integration")
    ]
    choices = serializers.SerializerMethodField()
    component = serializers.ChoiceField(choices=COMPONENT_CHOICES)

    def get_choices(self, obj):
        return [choice[0] for choice in self.COMPONENT_CHOICES]