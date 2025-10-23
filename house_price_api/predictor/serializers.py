# predictor/serializers.py
from rest_framework import serializers


class HousePredictionRequestSerializer(serializers.Serializer):
    """
    Serializer para validar los datos de entrada de la predicción.
    Define qué campos son obligatorios y sus tipos.
    """
    median_income = serializers.FloatField(
        min_value=0,
        help_text="Ingreso mediano del área (en $10k)"
    )
    house_age = serializers.FloatField(
        min_value=0,
        max_value=100,
        help_text="Edad de la casa en años"
    )
    average_rooms = serializers.FloatField(
        min_value=1,
        help_text="Número promedio de habitaciones"
    )
    average_bedrooms = serializers.FloatField(
        min_value=0.5,
        help_text="Número promedio de dormitorios"
    )
    population = serializers.FloatField(
        min_value=0,
        help_text="Población del área"
    )
    average_occupancy = serializers.FloatField(
        min_value=0.5,
        help_text="Ocupantes promedio por vivienda"
    )
    latitude = serializers.FloatField(
        min_value=32.5,
        max_value=42.0,
        help_text="Latitud (California: 32.5 - 42.0)"
    )
    longitude = serializers.FloatField(
        min_value=-124.5,
        max_value=-114.0,
        help_text="Longitud (California: -124.5 - -114.0)"
    )


class HousePredictionResponseSerializer(serializers.Serializer):
    """
    Serializer para estructurar la respuesta de la predicción.
    """
    predicted_price = serializers.FloatField(
        help_text="Precio predicho en dólares"
    )
    formatted_price = serializers.CharField(
        help_text="Precio formateado con separadores de miles"
    )
    confidence = serializers.CharField(
        help_text="Nivel de confianza de la predicción"
    )