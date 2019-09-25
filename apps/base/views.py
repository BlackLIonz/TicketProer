from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.feedbacks.serializers import ReviewSerializer


class ReviewsMixin(viewsets.GenericViewSet):

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        parent_object = self.get_object()
        reviews = list(parent_object.reviews.all())
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
