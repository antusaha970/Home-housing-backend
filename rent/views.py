from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from .serializers import *
from .models import *
from rest_framework.decorators import action, api_view, permission_classes, authentication_classes
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .filters import AdvertisementFilter
from rest_framework.pagination import PageNumberPagination
from django.db.models import Avg


class AdvertisementPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


class AdvertisementViewSet(viewsets.ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]
    pagination_class = AdvertisementPagination

    def get_queryset(self):

        filterset = AdvertisementFilter(
            self.request.GET, queryset=Advertisement.objects.filter(is_admin_approved=True).order_by('id'))
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

    @action(detail=True, methods=['GET'])
    def all_reviews(self, request, pk=None):
        review = AdvertisementReview.objects.filter(advertisement__id=pk)
        serializer = AdvertisementReviewSerializer(review, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def post_reviews(self, request, pk=None):
        data = request.data
        advertisement = get_object_or_404(Advertisement, pk=pk)
        serializer = ReviewSerializer(data=data, many=False)
        if serializer.is_valid():
            review = serializer.save()

            adReview = AdvertisementReview(
                review=review, advertisement=advertisement)
            adReview.save()

            rating = advertisement.advertisement_review.aggregate(
                avg_ratings=Avg('review__rating'))
            advertisement.rating = rating['avg_ratings']
            advertisement.save(update_fields=['rating'])

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'])
    def add_to_favorite(self, request, pk=None):
        """This method add a specific ad to favorite list"""
        user = request.user
        advertisement = get_object_or_404(Advertisement, pk=pk)
        is_already_added_to_favorite = UserFavoriteAdvertisement.objects.filter(
            advertisement=advertisement).exists()

        if is_already_added_to_favorite:
            return Response({"details": "Already added to Favorite"}, status=status.HTTP_201_CREATED)

        favorites = UserFavoriteAdvertisement(
            user=user, advertisement=advertisement)
        favorites.save()
        return Response({"details": "Added to Favorite"}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['DELETE'])
    def remove_from_favorite(self, request, pk=None):
        """This method removes a advertisement from favorites list"""
        user = request.user

        ad_to_remove = get_object_or_404(
            UserFavoriteAdvertisement, advertisement__id=pk)
        ad_to_remove.delete()

        return Response({"details": "Removed from Favorite"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAdminUser])
@authentication_classes([TokenAuthentication])
def all_advertisement_only_for_admin(request):
    """"This function shows all advertisement requests only for admin"""
    advertisements = Advertisement.objects.all()
    serializer = AdvertisementSerializer(advertisements, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
@authentication_classes([TokenAuthentication])
def approved_advertisement_request(request, pk=None):
    """This function approve  an advertisement request via pk. Only admin can approve a request"""
    advertisements = get_object_or_404(Advertisement, pk=pk)
    advertisements.is_admin_approved = True
    advertisements.save(update_fields=['is_admin_approved'])
    return Response({"details": "Approved rent advertisement request"})
