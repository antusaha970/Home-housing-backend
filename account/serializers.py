from rest_framework import serializers
from django.contrib.auth.models import User


class AccountSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name',
                  'last_name', 'password', 'confirm_password']
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'password': {'required': True},
            'confirm_password': {'required': True},
        }

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")

        if User.objects.filter(username=username, email=email).exists():
            raise serializers.ValidationError(
                "A user with that username/email already exists")

        return super().validate(attrs)

    def save(self, **kwargs):
        username = self.validated_data['username']
        email = self.validated_data['email']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        last_name = self.validated_data['last_name']
        password = self.validated_data['password']

        account = User(username=username, email=email,
                       first_name=first_name, last_name=last_name)

        account.set_password(password)
        account.is_active = False

        account.save()
        return account


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)

    class Meta:
        extra_kwargs = {
            'username': {'required': True},
            'password': {'required': True}
        }
