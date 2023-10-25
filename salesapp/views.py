# regions/views.py
from rest_framework import generics, mixins
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .api.serializers import SalespeopleSerializer, CommissionSerializer, CompanySerializer, CommissionDisplaySerializer
from .models import Salespeople, CommissionRate, Company


class SetCompanyView(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
):
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_object(self):
        c = Company.objects.first()
        if c:
            return c
        return Company.objects.create()


class SalespeopleListCreateView(generics.ListCreateAPIView):
    queryset = Salespeople.objects.all()
    serializer_class = SalespeopleSerializer
    permission_classes = [IsAuthenticated]


class SalespeopleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Salespeople.objects.all()
    serializer_class = SalespeopleSerializer
    permission_classes = [IsAdminUser]


class CreateCommissionView(CreateAPIView):
    serializer_class = CommissionSerializer
    permission_classes = [IsAuthenticated]


class RetrieveCommissionView(RetrieveAPIView):
    queryset = CommissionRate.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = CommissionDisplaySerializer

    def get_object(self):
        qs = self.get_queryset()
        return get_object_or_404(
            qs,
            year=self.request.query_params.get("year"),
            month=self.request.query_params.get("month"),
            sales_people__pk=self.request.query_params.get("sales_people"),
        )
