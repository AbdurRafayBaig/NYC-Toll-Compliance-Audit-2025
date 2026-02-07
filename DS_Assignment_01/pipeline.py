from src.data_pipeline import MetropolitanIngestor
from src.analytics import UrbanLogisticsEngine
from src.forecasting_engine import MetropolitanDemandForecaster

def main():
    """
    Master orchestration script for the Metropolitan Transit Impact Analysis.
    This pipeline synchronizes data acquisition, multi-dimensional analytics, 
    and predictive modeling.
    """
    print("--- METROPOLITAN TRANSPORTATION AUDIT PIPELINE v3.0 ---")
    
    # 1. Data Acquisition & Normalization
    # Handles remote asset retrieval, unification of disparate datasets, 
    # and sanitization of the transit logging lake.
    ingestor = MetropolitanIngestor()
    con = ingestor.run_full_lifecycle()
    
    # 2. Analytical Suite Execution
    # Runs the compliance audit, velocity matrix generation, 
    # and econometric modeling for the 2025 Congestion Relief Zone.
    engine = UrbanLogisticsEngine(con)
    engine.execute_analytical_suite()
    
    # 3. Predictive Modeling (Machine Learning)
    # Calibrates the Random Forest Regressor for infrastructure demand forecasting.
    predictor = MetropolitanDemandForecaster()
    ml_data = predictor.prepare_inference_features(con)
    predictor.train_forecasting_model(ml_data)
    
    print("\n[SUCCESS] Metropolitan lifecycle complete. Execute 'streamlit run dashboard.py' to initialize the UI.")

if __name__ == "__main__":
    main()
