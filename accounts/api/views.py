from rest_framework import permissions, viewsets
from django.contrib.auth.models import User
from accounts.api.serializers import UserSerializer

class UserViewSets(viewsets.ModelViewSet):
    users = User.objects.all().order_by('date_joined')
    serializer = UserSerializer(data=users)




