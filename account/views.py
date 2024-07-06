from django.shortcuts import render, redirect
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404


class RegisterAccountView(APIView):
    def post(self, request):
        """This method register an account and send email to user email"""
        data = request.data
        serializer = AccountSerializer(data=data, many=False)
        if serializer.is_valid():
            account = serializer.save()

            token = default_token_generator.make_token(account)
            uid = urlsafe_base64_encode(force_bytes(account.id))

            activation_link = f"Your account activation link:   http://127.0.0.1:8000/api/accounts/activate/{uid}/{token}/"

            send_mail("Account activation link", activation_link,
                      "noreplay@gmail.com", [account.email])

            return Response({'details': "Account activation link has been sent to user email"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, uuid64, token):
        """This method activate the account"""
        try:
            uid = urlsafe_base64_decode(uuid64).decode()
            user = User._default_manager.get(pk=uid)
        except (User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response("Account activated. You can close the tab and return to website")
        else:
            return redirect("Something went wrong! Please try again.")


class LoginAccountView(APIView):
    def post(self, request):
        data = request.data

        serializer = LoginSerializer(data=data, many=False)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            account = authenticate(username=username, password=password)

            if account:
                token, _ = Token.objects.get_or_create(user=account)
                account = AccountSerializer(account)
                return Response({'account': account.data, 'token': str(token)})

            return Response({"errors": "No user found with given credentials"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        user = request.user
        profile = get_object_or_404(Profile, user=user)
        serializer = ProfileSerializer(profile, many=False)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        profile_data = request.data
        profile_data['user'] = user.id

        serializer = ProfileSerializer(data=profile_data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        data = request.data
        serializer = ProfileSerializer(
            instance=profile, data=data, many=False, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
