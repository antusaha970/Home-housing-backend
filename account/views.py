from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import AccountSerializer
from rest_framework.response import Response
from rest_framework import status


class RegisterAccountView(APIView):
    def post(self, request):
        data = request.data
        serializer = AccountSerializer(data=data, many=False)
        if serializer.is_valid():
            account = serializer.save()
            print('Account', account)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
