# predictor/ml_service.py
import joblib
import numpy as np
from pathlib import Path
from typing import Dict, Tuple
import os


class HousePriceMLService:
    """
    Servicio que encapsula la lógica de Machine Learning.
    Patrón Singleton: solo carga el modelo UNA vez en memoria.
    """

    _instance = None
    _model = None

    def __new__(cls):
        """
        Implementa Singleton para evitar cargar el modelo múltiples veces.
        """
        if cls._instance is None:
            cls._instance = super(HousePriceMLService, cls).__new__(cls)
            cls._instance._load_model()
        return cls._instance

    def _load_model(self):
        """
        Carga el modelo pre-entrenado desde el archivo .pkl
        """
        # Ruta absoluta para evitar problemas
        base_dir = Path(__file__).parent
        model_path = base_dir / 'house_price_model.pkl'

        print(f"🔍 DEBUG: Buscando modelo en: {model_path.absolute()}")
        print(f"🔍 DEBUG: ¿Existe el archivo? {model_path.exists()}")

        # Listar archivos en la carpeta
        print(f"🔍 DEBUG: Archivos en {base_dir}:")
        for file in os.listdir(base_dir):
            print(f"  - {file}")

        if not model_path.exists():
            error_msg = (
                f"❌ Modelo no encontrado en {model_path.absolute()}\n"
                f"📁 Carpeta actual: {base_dir.absolute()}\n"
                f"💡 Solución: Ejecuta train_model_quick.py para crear el modelo"
            )
            print(error_msg)
            raise FileNotFoundError(error_msg)

        try:
            self._model = joblib.load(model_path)
            print(f"✅ Modelo cargado exitosamente desde {model_path}")
            print(f"🔍 DEBUG: Tipo de modelo: {type(self._model)}")
            print(f"🔍 DEBUG: ¿Modelo es None? {self._model is None}")
        except Exception as e:
            print(f"❌ Error al cargar modelo: {str(e)}")
            raise

    def predict_price(self, features: Dict[str, float]) -> Tuple[float, str]:
        """
        Predice el precio de una casa basándose en sus características.
        """
        print(f"🔍 DEBUG: En predict_price, modelo es None? {self._model is None}")

        if self._model is None:
            raise ValueError("El modelo no está cargado. Verifica los logs del servidor.")

        # Preparar features en el orden correcto
        feature_array = np.array([[
            features['median_income'],
            features['house_age'],
            features['average_rooms'],
            features['average_bedrooms'],
            features['population'],
            features['average_occupancy'],
            features['latitude'],
            features['longitude']
        ]])

        # Hacer predicción
        prediction = self._model.predict(feature_array)[0]

        # Convertir a dólares
        price_in_dollars = prediction * 100000

        # Calcular nivel de confianza
        confidence = self._calculate_confidence(price_in_dollars)

        return price_in_dollars, confidence

    def _calculate_confidence(self, price: float) -> str:
        """
        Calcula el nivel de confianza basándose en rangos de precios históricos.
        """
        if 50000 <= price <= 450000:
            return "Alta"
        elif 30000 <= price <= 500000:
            return "Media"
        else:
            return "Baja"