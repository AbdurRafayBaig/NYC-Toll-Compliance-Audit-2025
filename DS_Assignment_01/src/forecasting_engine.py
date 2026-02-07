import os
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pickle
from src.config import *

class MetropolitanDemandForecaster:
    """
    Predictive engine utilizing Random Forest Regression to estimate 
    metropolitan transit demand based on temporal and environmental features.
    """
    def __init__(self):
        self.model_path = os.path.join(OUTPUT_DIR, "traffic_model.pkl")
        self.model = self._load_persisted_model()

    def _load_persisted_model(self):
        """Loads the pre-trained regressor into memory during initialization."""
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, 'rb') as f:
                    return pickle.load(f)
            except:
                pass
        # Fallback to untrained model if persistence is unavailable
        return RandomForestRegressor(n_estimators=100, random_state=42)

    def prepare_inference_features(self, con):
        """Engineers a feature matrix for model training and cross-validation."""
        print("Synthesizing Predictive Feature Matrix...")
        query = """
            WITH daily AS (
                SELECT 
                    CAST(pickup_time AS DATE) as date,
                    COUNT(*) as trip_count,
                    dayofweek(pickup_time) as dow,
                    month(pickup_time) as month
                FROM trips_clean
                WHERE year(pickup_time) = 2025
                GROUP BY 1, 3, 4
            )
            SELECT d.*, w.precipitation_sum
            FROM daily d
            LEFT JOIN read_csv('output/weather_impact.csv') w ON d.date = w.date
        """
        try:
            df = con.execute(query).df()
            return df.dropna()
        except Exception as e:
            return pd.DataFrame()

    def train_forecasting_model(self, df):
        """Trains the regressor on the engineered feature matrix."""
        if df.empty or len(df) < 10:
            return False

        print(f"Calibrating Demand Forecaster on {len(df)} temporal nodes...")
        X = df[['dow', 'month', 'precipitation_sum']]
        y = df['trip_count']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        
        # Persist trained state
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.model, f)
        
        score = self.model.score(X_test, y_test)
        print(f"  [MODEL] Forecasting Calibration R^2: {score:.4f}")
        return True

    def generate_prediction(self, dow, month, precip):
        """Generates a volume estimate using the memory-resident model."""
        try:
            # Check if the model has been fitted before predicting
            if hasattr(self.model, 'n_features_in_'):
                # Pass feature names to avoid UserWarning and ensure consistency
                features = pd.DataFrame([[dow, month, precip]], 
                                     columns=['dow', 'month', 'precipitation_sum'])
                pred = self.model.predict(features)
                return int(pred[0])
        except Exception as e:
            print(f"Prediction Error: {e}")
        return 0

if __name__ == "__main__":
    pass
