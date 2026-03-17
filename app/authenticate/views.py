from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiRequest
from .models import User
from .serializers import UserSerializer
from crm_lite.permissions import IsCompanyOwner


class UserRegistrationView(CreateAPIView):
    permission_classes = []
    queryset = User.objects.all()
    serializer_class = UserSerializer

@extend_schema(
    description="Эндпоинт прикрепления сотрудников",
    tags=['users'],
    request=OpenApiRequest(
        request={
            "type": "object",
            "properties": {
                "email": {
                    "type": "string",
                    "example": "user@example.com"
                },
            }
        }
    )
)
class AttachUserView(APIView):
    permission_classes = [IsCompanyOwner]

    def put(self, request, pk=None, format=None):
        owner = request.user
        user = get_object_or_404(User, email=request.data['email'])
        if user.company_id:
            return Response('Пользователь уже привязан к компании', status=status.HTTP_403_FORBIDDEN)
        user.company_id = owner.company_id
        user.save()
        return Response('Пользователь успешно прикреплён', status=status.HTTP_200_OK)

@extend_schema(
    description="Эндпоинт открепления сотрудников",
    tags=['users'],
    request=OpenApiRequest(
        request={
            "type": "object",
            "properties": {
                "email": {
                    "type": "string",
                    "example": "user@example.com"
                },
            }
        }
    )
)
class UnattachUserView(APIView):
    permission_classes = [IsCompanyOwner]

    def put(self, request, pk=None, format=None):
        owner = request.user
        user = get_object_or_404(User, email=request.data['email'], company_id=owner.company_id)
        if user.is_company_owner:
            return Response('Нельзя открепить самого себя', status=status.HTTP_403_FORBIDDEN)
        user.company_id = None
        user.save()
        return Response('Пользователь успешно откреплён', status=status.HTTP_200_OK)

class StaffListView(ListAPIView):
    permission_classes = [IsCompanyOwner]

    def list(self, request):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        return User.objects.filter(company_id=self.request.user.company_id)