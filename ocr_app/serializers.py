# from rest_framework import serializers

# class ReceiptSerializer(serializers.Serializer):
#     date = serializers.CharField(required=False)
#     merchant = serializers.CharField(required=False)
#     total = serializers.CharField(required=False)
#     category = serializers.CharField(required=False)
#     items = serializers.ListField(child=serializers.DictField(), required=False)
#     raw_text = serializers.CharField(required=False)
#     error = serializers.CharField(required=False)

from rest_framework import serializers
import re

class ItemSerializer(serializers.Serializer):
    name = serializers.CharField(allow_null=True)
    quantity = serializers.FloatField(allow_null=True)
    unit_price = serializers.FloatField(allow_null=True)
    total = serializers.FloatField(allow_null=True)

class ReceiptSerializer(serializers.Serializer):
    merchant = serializers.CharField(allow_null=True)
    date = serializers.CharField(allow_null=True)  # Format: YYYY-MM-DD
    items = serializers.ListField(
        child=ItemSerializer(),
        allow_empty=True
    )
    total = serializers.FloatField(allow_null=True)
    category = serializers.ChoiceField(
        allow_null=True,
        choices=[
            "Food", "Income", "Housing", "Groceries",
            "Electronics", "Transportation", "Dining",
            "Healthcare", "Shopping", "Entertainment",
            "Utilities", "Other"
        ]
    )
    accuracy = serializers.FloatField(
        min_value=0,
        max_value=100,
        allow_null=True
    )
    
    # Optional: Add validation for date format
    def validate_date(self, value):
        if value and not re.match(r'^\d{4}-\d{2}-\d{2}$', value):
            raise serializers.ValidationError("Date must be in YYYY-MM-DD format")
        return value