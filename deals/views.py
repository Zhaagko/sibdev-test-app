from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework import status

from .repository import bulk_create_deals, get_top_spending_customers
from .serializers import (
    DealLoadSerializer,
    DealTopSpendingCustomerSerializer,
)
from .utils import deserialize_uploaded_csv_file
from .enums import ApiStatusEnum


class DealViewSet(CreateModelMixin, GenericViewSet):
    def create(self, request, *args, **kwargs) -> Response:
        uploaded_file = request.FILES.get("deals")

        if not uploaded_file:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "Status": ApiStatusEnum.ERROR.value,
                    "Desc": f"Запрос должен содержать файл deals.",
                },
            )

        deals_list = deserialize_uploaded_csv_file(uploaded_file)
        validated_list = DealLoadSerializer.get_validated_deals_list(deals_list)
        bulk_create_deals(validated_list)
        return Response(
            status=status.HTTP_201_CREATED, data={"status": ApiStatusEnum.OK.value}
        )

    def list(self, *args, **kwargs) -> Response:
        result = get_top_spending_customers()
        serializer = DealTopSpendingCustomerSerializer(data=result, many=True)
        serializer.is_valid()
        return Response(
            status=status.HTTP_200_OK,
            data={"status": ApiStatusEnum.OK.value, "result": serializer.data},
        )
