from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken

from .serializers import UserSerializer, RegisterSerializer

from django.contrib.auth import login

from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
# Register API


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = AuthToken.objects.create(user)
        token = data[1]
        expiry = data[0].expiry
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token,
            "expiry": expiry,
        })


# class LoginAPI(generics.GenericAPIView):
#     serializer_class = LoginSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data
#         return Response({
#             "user": UserSerializer(user, context=self.get_serializer_context()).data,
#             'expiry': get_expiry_datetime_format(self),
#             "token": AuthToken.objects.create(user)[1]
#         })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)
