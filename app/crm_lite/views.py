from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from drf_spectacular.utils import extend_schema, OpenApiRequest
from .models import Company, Storage
from .serializers import CompanySerializer, StorageSerializer #ProductSerializer
from .permissions import IsCompanyOwner



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

class RetrieveCompanyView(APIView):
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

class RetrieveStorageView(APIView):
    serializer_class = StorageSerializer

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


# @extend_schema(
#     description="Эндпоинт создания товара",
#     tags=['Products'],
#     # request=ProductSerializer,
#     request=OpenApiRequest(
#         request={
#             "type": "object",
#             "properties": {
#                 "storage": {
#                     "type": "integer",
#                     "example": 10
#                 },
#                 "title": {
#                     "type": "string",
#                     "example": "Игровая клавиатура"
#                 },
#                 "description": {
#                     "type": "string",
#                     "example": "Описание характеристик клавиатуры"
#                 },
#                 "purchase_price": {
#                     "type": "string",
#                     "example": "1200.25"
#                 },
#                 "sale_price": {
#                     "type": "string",
#                     "example": "2530.55"
#                 }
#             }
#         }
#     )
# )
#
# class CreateProductView(APIView):
#     def post(self, request):
#         serializer = ProductSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response (serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)