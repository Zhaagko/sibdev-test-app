from rest_framework import serializers, exceptions
from rest_framework.status import HTTP_400_BAD_REQUEST
from .models import Deal
from .enums import ApiStatusEnum


def get_validated_deals_list(deals_list: list[dict], serializer_class) -> list[Deal]:
    serializer: serializers.Serializer
    result: list[Deal] = []

    for ind in range(len(deals_list)):
        deal = deals_list[ind]
        serializer = serializer_class(data=deal)
        if not serializer.is_valid():
            raise exceptions.ValidationError(
                code=HTTP_400_BAD_REQUEST,
                detail={
                    "Status": ApiStatusEnum.ERROR.value,
                    "Desc": f"Строка {ind+1} имеет некорректный формат.",
                },
            )
        result.append(Deal(**serializer.data))

    return result


class DealSerializer(serializers.Serializer):
    customer = serializers.CharField()
    item = serializers.CharField()
    total = serializers.IntegerField()
    quantity = serializers.IntegerField()
    date = serializers.DateTimeField()

    def update(self, instance, validated_data):
        raise NotImplementedError

    def create(self, validated_data) -> Deal:
        raise NotImplementedError
