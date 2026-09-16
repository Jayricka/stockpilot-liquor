from rest_framework import serializers


class DashboardSerializer(serializers.Serializer):
    date = serializers.DateField()

    summary = serializers.DictField()

    sales_by_payment_method = serializers.ListField()

    top_products = serializers.ListField()

    low_stock_products = serializers.ListField()

    recent_sales = serializers.ListField()

    recent_purchases = serializers.ListField()
