from rest_framework.views import APIView 
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate 
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.middleware.csrf import get_token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.renderers import JSONRenderer
from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('access_token')
        
        if not token:
            raise AuthenticationFailed("Токен отсутствует")

        try:
            validated_token = self.get_validated_token(token)
            user = self.get_user(validated_token)
        except Exception as e:
            raise AuthenticationFailed(f"Ошибка аутентификации: {e}")

        return (user, validated_token) 


class LoginAPIView(APIView):
    renderer_classes = [JSONRenderer]
    
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')    

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            response = Response({"message": "Успешный вход"})
            
            response.set_cookie(
                key="access_token",
                value=str(refresh.access_token),
                httponly=False,
                secure=False, 
                samesite="Lax",
            )
            response.set_cookie(
                key="refresh_token",
                value=str(refresh),
                httponly=False,
                secure=False, 
                samesite="Lax",
            )
            
            response.data['csrf_token'] = get_token(request)
            response['Location'] = '/authenticated/'
            response.status_code = 302
            return response

        return render(request, 'login.html', {'error': 'Невалидные данные'})
    

class LogoutAPIView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request, *args, **kwargs):
        response = Response({"message": "Успешный выход"})
        
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response
    

class RefreshAccessTokenAPIView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({"error": "Refresh токен не предоставлен"}, status=400)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            response = Response({"access_token": access_token}, status=200)
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=False, 
                secure=False,   
                samesite="Lax"
            )
            return response
        except AuthenticationFailed as e:
            return Response({'error': str(e)}, status=401)
        except Exception as e:
            return Response({"error": "Невалидный refresh токен"}, status=401)