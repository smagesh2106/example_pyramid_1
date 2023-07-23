from rest_framework_simplejwt.views import TokenObtainPairView, TokenViewBase
from .serializers import MyTokenObtainPairSerializer, CustomUserSerializer, ChangePasswordSerializer, \
    CustomUserListSerializer
from rest_framework import generics, status, permissions, response, filters, pagination, response, serializers
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import CustomUser


# Create your views here.
class MyTokenObtainPairView(TokenViewBase):
    serializer_class = MyTokenObtainPairSerializer


# class RegisterView(APIView):
class RegisterView2(generics.CreateAPIView):
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


class UserPagination(pagination.LimitOffsetPagination):
    default_limit = 20
    max_limit = 100


class UserListView(generics.ListAPIView):
    permission_classes = (permissions.IsAdminUser,)
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserListSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ['name', 'email', 'date_of_birth']
    pagination_class = UserPagination


class UserDeleteView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAdminUser,)
    lookup_field = 'pk'
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserListSerializer


@api_view(['GET'])
def get_user(request, pk):
    if not request.user.is_admin:
        if request.user.id != pk:
            return response.Response(status=status.HTTP_403_FORBIDDEN, data={"error": "Only admin or owner can "
                                                                                      "view this obj."})
    user = get_object_or_404(CustomUser, pk=pk)
    data = CustomUserSerializer(user).data
    return response.Response(data)


"""
@api_view(['GET'])
def get_admins(request):
    if not request.user.is_admin:
        return response.Response(status=status.HTTP_403_FORBIDDEN, data={"error": "Only admins are allowed."})

    users = CustomUser.objects.filter(Q(is_admin=True) & Q(is_staff=True))
    print(users.count())
    data = CustomUserListSerializer(users, many=True).data
    return response.Response(data=data)
"""


class AdminUsers(generics.ListAPIView):
    permission_classes = (permissions.IsAdminUser,)
    queryset = CustomUser.objects.filter(Q(is_admin=True) & Q(is_staff=True))
    serializer_class = CustomUserListSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ['name', 'email', 'date_of_birth']
    pagination_class = UserPagination


@api_view(['PATCH'])
@parser_classes((JSONParser,))
def update_user(request, pk):
    if not request.user.is_admin:
        if request.user.id != pk:
            return response.Response(status=status.HTTP_403_FORBIDDEN)

    user = get_object_or_404(CustomUser, pk=pk)
    serializer = CustomUserSerializer(instance=user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return response.Response(serializer.data)
    else:
        return response.Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


@api_view(['PATCH'])
@parser_classes((JSONParser,))
def toggle_admin_previlege(request, pk):
    if not request.user.is_superuser:
        return response.Response(status=status.HTTP_403_FORBIDDEN)

    user = get_object_or_404(CustomUser, pk=pk)
    print(user._meta.get_field("is_admin"))
    is_admin = request.data.get("is_admin", False)
    is_staff = request.data.get("is_staff", False)
    data = {"is_admin": is_admin, "is_staff": is_staff}
    print(data)
    serializer = CustomUserSerializer(instance=user, data=request.data, partial=True)
    # serializer = CustomUserSerializer(instance=user, data=data, partial=True) #works
    if serializer.is_valid():
        serializer.save()
        return response.Response(serializer.data)
    else:
        return response.Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

"""
class UserDeleteView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAdminUser,)
    queryset = CustomUser.objects.all()


class UserDetailView(APIView):
    lookup_field = 'id'

    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        if not request.user.is_admin:
            u = request.user
            if u.id != pk:
                return HttpResponseForbidden()
        user = self.get_object(pk)
        serializer = CustomUserSerializer(user)
        return response.Response(serializer.data)



    def delete(self, request, pk):
        snippet = self.get_object(pk)
        snippet.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
        
        
@api_view(['GET'])
def get_users(request):
    if not request.user.is_admin:
        return response.Response(status=status.HTTP_403_FORBIDDEN)

    users = None
    # checking for the parameters from the URL
    query = request.query_params.get('search')
    print("query  :"+query)
    if request.query_params:
        users = CustomUser.objects.filter(**request.query_params.dict())
    else:
        users = CustomUser.objects.all()

    # if there is something in items else raise error
    if users:
        page_number = request.query_params.get('offset', 1)
        page_size = request.query_params.get('limit', 2)

        paginator = Paginator(users, page_size)
        serializer = CustomUserSerializer(paginator.page(page_number), many=True, context={'request': request})
        #serializer = CustomUserSerializer(users, many=True)
        return response.Response(serializer.data)
    else:
        return response.Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_user(request, pk):
    if not request.user.is_admin:
        return response.Response(status=status.HTTP_403_FORBIDDEN)

    user = None
    try:
        user = CustomUser.objects.get(pk=pk)
    except CustomUser.DoesNotExist:
        return response.Response(status=status.HTTP_404_NOT_FOUND)
    user.delete()
    return response.Response(status=status.HTTP_202_ACCEPTED)

"""
