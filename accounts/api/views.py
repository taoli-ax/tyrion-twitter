from rest_framework import permissions, viewsets
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import (
    login as django_login,
    logout as django_logout,
    authenticate as django_authenticated
)
from accounts.api.serializers import UserSerializer, SignUpSerializer, LoginSerializer


class UserViewSet(viewsets.ModelViewSet):
    users = User.objects.all().order_by('date_joined')
    serializer = UserSerializer(data=users)
    permission_classes = (IsAuthenticated,)


class AccountsViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer

    @action(methods=['POST'],detail=False)
    def signup(self,request):
        serializer = SignUpSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': 'Please checkout input.',
                'error': serializer.errors
            },status=400)
        user = serializer.save()

        return Response({
            'success':True,
            'user':UserSerializer(user).data
        })

    @action(methods=['POST'],detail=False)
    def login(self,request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'message':'Please check input.',
                'error':serializer.errors
            })
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user=User.objects.get(username=username)
        print(user.password)
        authenticated_user = django_authenticated(username=username,password=password)
        if not authenticated_user or authenticated_user.is_anonymous:
            return Response({
                'success': False,
                'message': 'user does not exist!'
            },status=400)
        django_login(request,user=authenticated_user)
        return Response({
            'success':True,
            'message': UserSerializer(instance=authenticated_user).data
        })

    @action(methods=['POST'],detail=False)
    def logout(self,request):
        django_logout(request)
        return Response({'success': True})

    @action(methods=['GET'],detail=False)
    def login_status(self,request):
        data ={'status':request.user.is_authenticated}
        if request.user.is_authenticated:
            data['user'] = UserSerializer(request.user).data
        return Response(data)

