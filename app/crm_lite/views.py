from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiRequest
from .models import Company, Storage, Supplier, Supply, Product, SupplyProduct
from .serializers import CompanySerializer, StorageSerializer, SupplierSerializer, CreateSupplySerializer, ListSupplySerializer, ProductSerializer, ProductUpdateSerializer
from .permissions import IsCompanyOwner, IsCompanyStaff



class CreateCompanyView(APIView):
    serializer_class = CompanySerializer

    def post(self, request):
        user = request.user
        if user.company_id:
            return Response('Пользователь уже привязан к компании', status=status.HTTP_403_FORBIDDEN)
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            company = serializer.save()
            user.is_company_owner = True
            user.company_id = company
            user.save()
            return Response (serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetCompanyByIdView(APIView):
    serializer_class = CompanySerializer

    def get(self, request, pk):
        company = get_object_or_404(Company, id=pk)
        return Response(CompanySerializer(company).data, status=status.HTTP_200_OK)

class UpdateCompanyView(APIView):
    serializer_class = CompanySerializer
    permission_classes = [IsCompanyOwner]

    def put(self, request, format=None):
        company = get_object_or_404(Company, id=request.user.company_id.id)
        serializer = CompanySerializer(company, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteCompanyView(APIView):
    serializer_class = CompanySerializer
    permission_classes = [IsCompanyOwner]

    def delete(self, request, format=None):
        user = request.user
        company = get_object_or_404(Company, id=user.company_id.id)
        user.is_company_owner = False
        user.save()
        company.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateStorageView(APIView):
    serializer_class = StorageSerializer
    permission_classes = [IsCompanyOwner]

    def post(self, request):
        user = request.user
        if user.company_id.storage.all():
            return Response('К вашей компании уже прикреплен склад', status=status.HTTP_403_FORBIDDEN)
        serializer = StorageSerializer(data=request.data)
        if serializer.is_valid():
            storage = Storage.objects.create(address=serializer.data['address'], company_id=user.company_id)
            return Response(StorageSerializer(storage).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetStorageByIdView(APIView):
    serializer_class = StorageSerializer
    permission_classes = [IsCompanyStaff]

    def get(self, request, pk):
        storage = get_object_or_404(Storage, id=pk, company_id=request.user.company_id)
        return Response(StorageSerializer(storage).data, status=status.HTTP_200_OK)

class UpdateStorageView(APIView):
    serializer_class = StorageSerializer
    permission_classes = [IsCompanyOwner]

    def put(self, request, pk, format=None):
        storage = get_object_or_404(Storage, id=pk, company_id=request.user.company_id)
        serializer = StorageSerializer(storage, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteStorageView(APIView):
    serializer_class = StorageSerializer
    permission_classes = [IsCompanyOwner]

    def delete(self, request, pk, format=None):
        storage = get_object_or_404(Storage, id=pk, company_id=request.user.company_id)
        storage.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class CreateSupplierView(APIView):
    serializer_class = SupplierSerializer
    permission_classes = [IsCompanyStaff]

    def post(self, request):
        serializer = SupplierSerializer(data=request.data)
        if serializer.is_valid():
            supplier = Supplier.objects.create(INN=serializer.data['INN'], title=serializer.data['title'], company_id=request.user.company_id)
            return Response(SupplierSerializer(supplier).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListSuppliersView(APIView):
    serializer_class = SupplierSerializer
    permission_classes = [IsCompanyStaff]

    def get(self, request):
        queryset = self.get_queryset()
        serializer = SupplierSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        return Supplier.objects.filter(company_id=self.request.user.company_id)


class UpdateSupplierView(APIView):
    serializer_class = SupplierSerializer
    permission_classes = [IsCompanyStaff]

    def put(self, request, pk, format=None):
        supplier = get_object_or_404(Supplier, id=pk, company_id=request.user.company_id)
        serializer = SupplierSerializer(supplier, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteSupplierView(APIView):
    serializer_class = SupplierSerializer
    permission_classes = [IsCompanyStaff]

    def delete(self, request, pk, format=None):
        supplier = get_object_or_404(Supplier, id=pk, company_id=request.user.company_id)
        supplier.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CreateSupplyView(APIView):
    serializer_class = CreateSupplySerializer
    permission_classes = [IsCompanyStaff]

    def post(self, request):
        get_object_or_404(Supplier, id=request.data['supplier_id'], company_id=request.user.company_id)
        serializer = CreateSupplySerializer(data=request.data)
        if serializer.is_valid():
            products = serializer.validated_data.pop('products')
            for product in products:
                p = get_object_or_404(Product, id=product['id'], storage_id__company_id=request.user.company_id)
                p.quantity += product['quantity']
                p.save()
            supply = serializer.save()
            SupplyProduct.objects.bulk_create([SupplyProduct(supply_id=supply, product_id=get_object_or_404(Product, id=product['id']), quantity=product['quantity']) for product in products])
            return Response(f'Поставка успешно создана (id = {supply.id})', status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListSuppliesView(APIView):
    serializer_class = ListSupplySerializer
    permission_classes = [IsCompanyStaff]

    def get(self, request):
        queryset = self.get_queryset()
        serializer = ListSupplySerializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        return Supply.objects.filter(supplier_id__company_id=self.request.user.company_id)

@extend_schema(
    description="Эндпоинт создания товара",
    #tags=['product'],
    request=OpenApiRequest(
        request={
            "type": "object",
            "properties": {
                "storage_id": {
                    "type": "integer",
                    "example": 10
                },
                "title": {
                    "type": "string",
                    "example": "Игровая клавиатура"
                },
                "description": {
                    "type": "string",
                    "example": "Описание характеристик клавиатуры"
                },
                "purchase_price": {
                    "type": "string",
                    "example": "1200.25"
                },
                "sale_price": {
                    "type": "string",
                    "example": "2530.55"
                }
            }
        }
    )
)
class CreateProductView(APIView):
    permission_classes = [IsCompanyStaff]

    def post(self, request):
        get_object_or_404(Storage, id=request.data['storage_id'], company_id=request.user.company_id)
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListProductsView(APIView):
    serializer_class = ProductSerializer
    permission_classes = [IsCompanyStaff]

    def get(self, request):
        queryset = self.get_queryset()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        return Product.objects.filter(storage_id__company_id=self.request.user.company_id)

class GetProductByIdView(APIView):
    serializer_class = ProductSerializer
    permission_classes = [IsCompanyStaff]

    def get(self, request, pk):
        product = get_object_or_404(Product, id=pk, storage_id__company_id=self.request.user.company_id)
        return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)

class UpdateProductView(APIView):
    serializer_class = ProductUpdateSerializer
    permission_classes = [IsCompanyStaff]

    def put(self, request, pk, format=None):
        product = get_object_or_404(Product, id=pk, storage_id__company_id=request.user.company_id)
        serializer = ProductUpdateSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteProductView(APIView):
    serializer_class = ProductSerializer
    permission_classes = [IsCompanyStaff]

    def delete(self, request, pk, format=None):
        product = get_object_or_404(Product, id=pk, storage_id__company_id=request.user.company_id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)