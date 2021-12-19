from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'date_joined')


class UserSerializerForTweet(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class SignUpSerializer(serializers.ModelSerializer):
    # check data valid and not used
    username = serializers.CharField(min_length=6, max_length=20)
    password = serializers.CharField(min_length=6, max_length=20)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def validate(self, attrs):
        username = attrs['username']
        email = attrs['email']
        if User.objects.filter(username=username.lower()).exists():
            raise ValidationError('this name has been occupied!')
        if User.objects.filter(email=email.lower()).exists():
            raise ValidationError('this email has benn occupied!')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'].lower(),
            email=validated_data['email'].lower(),
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'password')

    # def validate(self, attrs):
    #     if not User.objects.filter(username=attrs['username'].lower()).exists():
    #         raise ValidationError('username or password not correct,please check input')
    #     return attrs
