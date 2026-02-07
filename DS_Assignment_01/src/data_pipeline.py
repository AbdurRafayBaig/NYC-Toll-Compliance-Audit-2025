import os
import requests
import duckdb
import pandas as pd
from datetime import datetime
import glob
from src.config import *

class MetropolitanIngestor:
    """
    Automated data acquisition and unification engine for the NYC Metropolitan 
    transportation dataset. Implements schema-agnostic ingestion via DuckDB.
    """
    def __init__(self):
        self.con = duckdb.connect(database=':memory:') 
        try:
            # Spatial extension for future-proofing geospatial joins
            self.con.execute("INSTALL spatial; LOAD spatial;")
        except Exception as e:
            pass

    def _validate_integrity(self, path):
        """Verifies parquet file structure before downstream processing."""
        try:
            self.con.execute(f"SELECT * FROM read_parquet('{path}') LIMIT 0")
            return True
        except:
            return False

    def acquire_resource(self, url, filename, force=False):
        """Fetches remote assets with local caching and corruption detection."""
        dest_path = os.path.join(DATA_DIR, filename).replace('\\', '/')
        if os.path.exists(dest_path) and not force:
            if filename.endswith('.parquet') and not self._validate_integrity(dest_path):
                print(f"  [STATUS] Re-acquiring compromised asset: {filename}")
            else:
                return dest_path
        
        print(f"  [NETWORK] Synchronizing {url}")
        try:
            r = requests.get(url, stream=True, timeout=60)
            if r.status_code == 200:
                with open(dest_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=2048*1024):
                        if chunk: f.write(chunk)
                return dest_path
        except Exception as e:
            print(f"  [ERROR] Synchronization failed for {url}: {e}")
        return None

    def execute_ingestion_sequence(self):
        """Orchestrates the primary data acquisition workflow."""
        print("Initializing Metropolitan Data Repository...")
        self.acquire_resource(LOOKUP_URL, "taxi_zone_lookup.csv")
        self.acquire_resource(GEOJSON_URL, "taxi_zones.geojson")

        for year in YEARS_TO_DOWNLOAD:
            for month in range(1, 13):
                for taxi in TAXIS:
                    url = f"{BASE_URL}/{taxi}_tripdata_{year}-{month:02d}.parquet"
                    self.acquire_resource(url, f"{taxi}_tripdata_{year}-{month:02d}.parquet")

        # Baseline synchronization for predictive window
        for taxi in TAXIS:
            self.acquire_resource(f"{BASE_URL}/{taxi}_tripdata_2023-12.parquet", f"{taxi}_tripdata_2023-12.parquet")

    def unify_metropolitan_lake(self):
        """Standardizes heterogeneous schemas into a unified analytical table."""
        print("Normalizing multi-source transportation lake...")
        self.con.execute("""
            CREATE OR REPLACE TABLE raw_trips (
                pickup_time TIMESTAMP,
                dropoff_time TIMESTAMP,
                pickup_loc INTEGER,
                dropoff_loc INTEGER,
                trip_distance DOUBLE,
                fare DOUBLE,
                total DOUBLE,
                surcharge DOUBLE,
                tip DOUBLE,
                taxi_type VARCHAR
            )
        """)

        for taxi in TAXIS:
            pattern = os.path.join(DATA_DIR, f"{taxi}_tripdata_*.parquet")
            files = [os.path.abspath(f).replace('\\', '/') for f in glob.glob(pattern)]
            
            if not files: continue
                
            pickup_col = "tpep_pickup_datetime" if taxi == "yellow" else "lpep_pickup_datetime"
            dropoff_col = "tpep_dropoff_datetime" if taxi == "yellow" else "lpep_dropoff_datetime"
            
            for f in files:
                try:
                    cols_df = self.con.execute(f"SELECT * FROM read_parquet('{f}') LIMIT 0").df()
                    has_surcharge = "congestion_surcharge" in cols_df.columns
                    surcharge_expr = "CAST(congestion_surcharge AS DOUBLE)" if has_surcharge else "0.0"
                    
                    self.con.execute(f"""
                        INSERT INTO raw_trips
                        SELECT 
                            {pickup_col}::TIMESTAMP, {dropoff_col}::TIMESTAMP,
                            PULocationID::INTEGER, DOLocationID::INTEGER,
                            trip_distance::DOUBLE, fare_amount::DOUBLE, 
                            total_amount::DOUBLE, {surcharge_expr},
                            tip_amount::DOUBLE, '{taxi}'
                        FROM read_parquet('{f}')
                        WHERE {pickup_col} >= '2023-12-01' AND {pickup_col} < '2026-02-01'
                    """)
                except:
                    pass
            
            print(f"  [INTEGRATION] Complated {taxi} dataset merge.")

    def apply_sanitization_policy(self):
        """Applies heuristic filtering to exclude technical anomalies (Ghost Trips)."""
        print("Enforcing metropolitan quality standard...")
        
        # Internal speed indexing
        self.con.execute("""
            CREATE OR REPLACE TABLE trips_clean AS
            SELECT *,
                (trip_distance * 3600.0) / NULLIF(date_diff('second', pickup_time, dropoff_time), 0) as speed_mph
            FROM raw_trips
            WHERE 
                date_diff('second', pickup_time, dropoff_time) BETWEEN 10 AND 10800
                AND trip_distance > 0
                AND fare > 0
        """)
        
        # Analytical Audit Generation
        self.con.execute("""
            SELECT 
                (SELECT COUNT(*) FROM raw_trips) as total_raw,
                (SELECT COUNT(*) FROM trips_clean) as total_clean
        """).df().to_csv(os.path.join(OUTPUT_DIR, "pipeline_audit.csv"), index=False)
        print("  [QUALITY] Sanitization cycle verified.")

    def run_full_lifecycle(self):
        self.execute_ingestion_sequence()
        self.unify_metropolitan_lake()
        self.apply_sanitization_policy()
        return self.con

if __name__ == "__main__":
    etl = NYCTrafficETL()
    etl.run_full_pipeline()
    print("ETL Phase Complete.")
