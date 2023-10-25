from rest_framework import serializers
from salesapp.models import Salespeople, CommissionRate, Company


class CompanySerializer(serializers.Serializer):
    name = serializers.CharField()
    logo = serializers.ImageField()

    def create(self, validated_data):
        c = Company.objects.first()
        if c:
            c.name = validated_data["name"]
            c.logo = validated_data["logo"]
            c.save()
            return c
        return Company.objects.create(**validated_data)


class SalespeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salespeople
        fields = ("id", 'name', 'number', 'photo', 'main_region',)


class CommissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommissionRate
        fields = (
            "id",
            "south_sales",
            "coast_sales",
            "north_sales",
            "east_sales",
            "lebanon_sales",
            "sales_people",
            "year",
            "month",
            "total_commission",
        )
        read_only_fields = (
            "id",
            "total_commission",
        )

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.calculate_commission()
        return instance


class CommissionDisplaySerializer(CommissionSerializer):
    sales_people = SalespeopleSerializer(read_only=True)

    class Meta:
        model = CommissionRate
        fields = (
            "id",
            "south_sales",
            "coast_sales",
            "north_sales",
            "east_sales",
            "lebanon_sales",
            "sales_people",
            "year",
            "month",
            "total_commission",
        )
        read_only_fields = (
            "id",
            "total_commission",
        )
