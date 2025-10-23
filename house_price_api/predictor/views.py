from django.shortcuts import render

# Create your views here.
# predictor/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import (
    HousePredictionRequestSerializer,
    HousePredictionResponseSerializer
)
from .ml_service import HousePriceMLService


class PredictHousePriceView(APIView):
    """
    API endpoint para predecir el precio de una casa.
    """

    @swagger_auto_schema(
        operation_description="Predice el precio de una casa basándose en 8 características",
        request_body=HousePredictionRequestSerializer,
        responses={
            200: HousePredictionResponseSerializer,
            400: "Datos de entrada inválidos"
        }
    )
    def post(self, request):
        """
        Endpoint POST para realizar predicciones.

        Flujo:
        1. Validar datos de entrada
        2. Llamar al servicio ML
        3. Retornar predicción formateada
        """
        # Validar datos de entrada con el serializer
        serializer = HousePredictionRequestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Obtener instancia del servicio ML (Singleton)
            ml_service = HousePriceMLService()

            # Realizar predicción
            predicted_price, confidence = ml_service.predict_price(
                serializer.validated_data
            )

            # Preparar respuesta
            response_data = {
                'predicted_price': predicted_price,
                'formatted_price': f"${predicted_price:,.2f}",
                'confidence': confidence
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Error en predicción: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class HealthCheckView(APIView):
    """
    Endpoint para verificar que el servicio está funcionando.
    """

    @swagger_auto_schema(
        operation_description="Verifica el estado del servicio y del modelo ML"
    )
    def get(self, request):
        """
        Retorna el estado del servicio.
        """
        try:
            ml_service = HousePriceMLService()
            return Response({
                "status": "healthy",
                "model_loaded": ml_service._model is not None,
                "version": "1.0.0"
            })
        except Exception as e:
            return Response(
                {"status": "unhealthy", "error": str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )