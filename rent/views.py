from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from .serializers import *
from .models import *
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .filters import AdvertisementFilter


class AdvertisementViewSet(viewsets.ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):

        filterset = AdvertisementFilter(
            self.request.GET, queryset=Advertisement.objects.all().order_by('id'))
        return filterset.qs

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user)

    @action(detail=True, methods=['POST'])
    def upload_image(self, request, pk=None):
        advertisement = get_object_or_404(Advertisement, pk=pk)

        images = request.FILES.getlist('images')
        serialized_data = []

        for img in images:
            data = {'advertisement': advertisement.id, 'image': img}
            serialized_data.append(data)

        serializer = AdvertiseImageSerializer(data=serialized_data, many=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'details': "Image uploaded successfully"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
