from flask import Flask, request, jsonify
import joblib
import numpy as np
import pandas as pd
from flask_cors import CORS



app = Flask(__name__)
CORS(app)
# Charger les deux modèles complets (avec scaler et features)
model_local_dict = joblib.load("model_local_complete.pkl")
model_export_dict = joblib.load("model_export_complete.pkl")

# Extraire modèles et scalers
model_local = model_local_dict['model']
scaler_local = model_local_dict['scaler']
features_local = model_local_dict['features']  # ['trend', 'month_sin', 'month_cos', 'quarter', 'ma3', 'lag1']

model_export = model_export_dict['model']
scaler_export = model_export_dict['scaler']
features_export = model_export_dict['features']

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    
    date_fin = data.get('dateFin')  # on utilise juste la date_fin pour prédiction
    type_ca = data.get('type')      # "local" ou "export"

    if not date_fin or not type_ca:
        return jsonify({"error": "Champs manquants"}), 400

    # Convertir la date en objet datetime
    date_fin_dt = pd.to_datetime(date_fin)
    month = date_fin_dt.month
    trend = (date_fin_dt - pd.Timestamp('2025-01-01')).days  # exemple de trend depuis début 2025
    month_sin = np.sin(2 * np.pi * month / 12)
    month_cos = np.cos(2 * np.pi * month / 12)
    quarter = (month - 1) // 3 + 1

    # Si pas d'historique, mettre 0 pour ma3 et lag1
    ma3 = 0
    lag1 = 0

    # Créer le DataFrame avec les features
    df_input = pd.DataFrame([[trend, month_sin, month_cos, quarter, ma3, lag1]],
                            columns=features_local)  # features_local et features_export identiques

    # Appliquer le scaler
    if type_ca == "local":
        df_scaled = scaler_local.transform(df_input)
        prediction = model_local.predict(df_scaled).item()
    elif type_ca == "export":
        df_scaled = scaler_export.transform(df_input)
        prediction = model_export.predict(df_scaled).item()
    else:
        return jsonify({"error": "Type inconnu"}), 400

    return jsonify({"prediction": prediction})

if __name__ == '__main__':
    app.run(debug=True)
