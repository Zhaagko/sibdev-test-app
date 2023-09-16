from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework import status

from .models import Deal
from .serializers import DealSerializer, get_validated_deals_list
from .utils import deserialize_uploaded_csv_file


class DealViewSet(CreateModelMixin, GenericViewSet):
    queryset = Deal.objects.none()
    serializer_class = DealSerializer

    def create(self, request, *args, **kwargs) -> Response:
        uploaded_file = request.FILES.get("deals")

        if not uploaded_file:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "You should pass the deals file."},
            )

        deals_list = deserialize_uploaded_csv_file(uploaded_file)
        validated_list = get_validated_deals_list(deals_list, self.serializer_class)

        Deal.objects.bulk_create(validated_list)

        return Response(status=status.HTTP_201_CREATED, data={"status": "OK"})
