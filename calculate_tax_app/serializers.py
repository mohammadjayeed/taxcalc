from rest_framework import serializers

class TaxCalculationSerializer(serializers.Serializer):
    street = serializers.CharField(max_length=150)
    city = serializers.CharField(max_length=150)
    state = serializers.CharField(max_length=150)
    zip = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    shipping = serializers.CharField(max_length=150, required=False)

    def validate_amount(self, value):
        if value < 1:
            raise serializers.ValidationError("amount must be a greater than 0.")
        return value
    
    def validate_city(self, value):
        if any(char.isdigit() for char in value):
            raise serializers.ValidationError("invalid city name")
        else:
            return value
    
    def validate_state(self, value):
        if len(value) > 2:
            raise serializers.ValidationError("Please enter a valid state code. e.g. NY for New York")
        else:
            return value