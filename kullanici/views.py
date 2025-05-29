from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from .serializers import RegisterSerializer, LoginSerializer
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.password_validation import validate_password, ValidationError

# Kayıt İşlemi
class RegisterAPI(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Kullanıcı kaydedilir
            login(request, user)  # Kullanıcı otomatik olarak giriş yapar
            token, _ = Token.objects.get_or_create(user=user)  # Token oluşturulur
            return Response({
                "message": "Kayıt başarılı!",
                "token": token.key,  # Token döndürülür
                "user": {
                    "id": user.id,
                    "email": user.email,
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Giriş İşlemi
class LoginAPI(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                token, _ = Token.objects.get_or_create(user=user)
                return Response({"token": token.key, "message": "Giriş başarılı!"}, status=status.HTTP_200_OK)
            return Response({"error": "Geçersiz kimlik bilgileri."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Çıkış İşlemi
class LogoutAPI(APIView):
    def post(self, request):
        request.user.auth_token.delete()  # Token silinir
        logout(request)
        return Response({"message": "Başarıyla çıkış yaptınız."}, status=status.HTTP_200_OK)

class PasswordChangeAPI(APIView):
    permission_classes = [IsAuthenticated]  # Sadece doğrulanmış kullanıcılar erişebilir

    def post(self, request):
        user = request.user

        # Gelen veriler
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        # Mevcut şifre doğrulama
        if not user.check_password(current_password):
            return Response({"error": "Mevcut şifre yanlış."}, status=status.HTTP_400_BAD_REQUEST)

        # Yeni şifrelerin eşleştiğini kontrol etme
        if new_password != confirm_password:
            return Response({"error": "Yeni şifreler eşleşmiyor."}, status=status.HTTP_400_BAD_REQUEST)

        # Yeni şifrenin doğrulama kurallarına uygunluğunu kontrol etme
        try:
            validate_password(new_password, user=user)
        except ValidationError as e:
            return Response({"error": e.messages}, status=status.HTTP_400_BAD_REQUEST)

        # Şifreyi değiştirme
        user.set_password(new_password)
        user.save()

        return Response({"message": "Şifre başarıyla değiştirildi."}, status=status.HTTP_200_OK)
