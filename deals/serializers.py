from rest_framework import serializers, exceptions
from rest_framework.status import HTTP_400_BAD_REQUEST
from .models import Deal
from .enums import ApiStatusEnum


class DealLoadSerializer(serializers.Serializer):
    customer = serializers.CharField()
    item = serializers.CharField()
    total = serializers.IntegerField()
    quantity = serializers.IntegerField()
    date = serializers.DateTimeField()

    @classmethod
    def get_validated_deals_list(cls, deals_list: list[dict]) -> list[Deal]:
        serializer: DealLoadSerializer
        result: list[Deal] = []

        for ind in range(len(deals_list)):
            deal = deals_list[ind]
            serializer = cls(data=deal)
            if not serializer.is_valid():
                raise exceptions.ValidationError(
                    code=HTTP_400_BAD_REQUEST,
                    detail={
                        "Status": ApiStatusEnum.ERROR.value,
                        "Desc": f"Строка {ind + 1} имеет некорректный формат.",
                    },
                )
            result.append(Deal(**serializer.data))

        return result

    def update(self, instance, validated_data):
        raise NotImplementedError

    def create(self, validated_data):
        raise NotImplementedError


class DealTopSpendingCustomerSerializer(serializers.Serializer):
    username = serializers.CharField()
    spent_money = serializers.IntegerField()
    gems = serializers.SerializerMethodField()

    def get_gems(self, deal: Deal) -> list[str]:
        gems = deal.gems
        return gems.split(",")

    def update(self, instance, validated_data):
        raise NotImplementedError

    def create(self, validated_data):
        raise NotImplementedError
