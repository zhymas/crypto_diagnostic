from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .serializers import UserRegisterSerializer, UserTokenSerializer, CustomTokenSerializer
from rest_framework import status


class UserRegisterView(APIView):

    @swagger_auto_schema(
        operation_description="Registed a new user",
        request_body=UserRegisterSerializer,
        responses={
            200: 'User registered successfully',
            400: 'Invalid input data',
        },
        examples={
            'application/json': {
                'username': 'testuser',
                'password': 'testpassword',
                'email': 'testuser@example.com',
            }
        }
    )
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'})
        return Response(serializer.errors, status=400)

class GetTokens(APIView):
    
    @swagger_auto_schema(
        operation_description="Get tokens",
        request_body=UserTokenSerializer,
        responses={
            200: 'User logged successfully',
            400: 'Invalid input data',
        },
        examples={
            'application/json': {
                'username': '',
                'password': ''
            }
        }
    )
    def post(self, request):
        serializer = UserTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh_token = CustomTokenSerializer().get_token(user)
            access_token = refresh_token.access_token
            
            return Response({
                'access': str(refresh_token),
                'refresh': str(access_token)
        })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)