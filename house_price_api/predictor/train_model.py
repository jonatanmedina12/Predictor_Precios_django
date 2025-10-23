# predictor/train_model.py
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib

print("🚀 Entrenando modelo de predicción de precios...")

# Cargar datos
housing = fetch_california_housing(as_frame=True)
X = housing.data
y = housing.target

# Dividir datos
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Entrenar modelo
model = LinearRegression()
model.fit(X_train, y_train)

# Guardar modelo en la MISMA carpeta
joblib.dump(model, 'house_price_model.pkl')

# Verificar
score = model.score(X_test, y_test)
print(f"✅ Modelo entrenado y guardado exitosamente!")
print(f"📊 Precisión (R²): {score:.4f}")
print(f"📁 Ubicación: {__file__}")

# Confirmar que existe
import os
if os.path.exists('house_price_model.pkl'):
    print("✅ Archivo house_price_model.pkl creado correctamente")
else:
    print("❌ ERROR: No se pudo crear el archivo")