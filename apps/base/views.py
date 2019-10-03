from django.utils.decorators import method_decorator
from drf_yasg.openapi import Response as SwgResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.feedbacks.serializers import ReviewSerializer


@method_decorator(name='reviews', decorator=swagger_auto_schema(
    operation_summary='List method that gives information about all reviews.',
    operation_description="""Gives detailed information about all reviews.
                             This endpoint is reachable by any.""",
    responses={
        '200': SwgResponse('Ok. Reviews returned.', ReviewSerializer()),
        '404': 'Not found. Bad id.',
    }
    )
)
class ReviewsMixin(viewsets.GenericViewSet):

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        parent_object = self.get_object()
        reviews = list(parent_object.reviews.all())
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
