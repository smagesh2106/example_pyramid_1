from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenViewBase
from .serializers import MyTokenObtainPairSerializer, CustomUserSerializer, ChangePasswordSerializer
from rest_framework import generics, status, permissions, response, filters, pagination, response, serializers
from .models import CustomUser


# Create your views here.
class MyTokenObtainPairView(TokenViewBase):
    serializer_class = MyTokenObtainPairSerializer


# class RegisterView(APIView):
class RegisterView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)  # required for new user registration
    serializer_class = CustomUserSerializer
    model = CustomUser

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data)


# Password change View
class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)

    class Meta:
        model = CustomUser

    def __init__(self):
        super().__init__()
        self.object = None

    def get_object(self, queryset=None):
        obj = self.request.user  # because we are going to update the user obj
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password

            if not self.object.check_password(serializer.data.get("old_password")):
                return response.Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            resp = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }
            return response.Response(resp)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
