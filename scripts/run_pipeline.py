import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.join(__file__, ".."))))
from app.pipeline import run_daily_pipeline

if __name__ == "__main__":
    run_daily_pipeline(
        concerts_csv="data/concerts.csv",
        interactions_csv="data/interactions.csv",
    )
    print("Pipeline run complete")
