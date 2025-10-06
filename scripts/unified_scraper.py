import os
import sys
import subprocess
from datetime import datetime
import argparse

def run_scraper(script_name: str, artist_name: str, output_file: str) -> bool:
    try:
        result = subprocess.run([
            sys.executable, script_name, artist_name, output_file
        ], capture_output=True, text=True, check=True)
        print(f"\u2713 {script_name}: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\u2717 {script_name}: {e.stderr.strip()}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Unified scraper for multiple data sources")
    parser.add_argument("artist", help="Artist name to scrape")
    parser.add_argument("--output-dir", default="data", help="Output directory for CSV files")
    parser.add_argument("--sources", nargs="+",
                       choices=["seatgeek", "bandsintown", "social", "streaming"],
                       default=["seatgeek", "bandsintown", "social", "streaming"],
                       help="Data sources to scrape")

    args = parser.parse_args()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = args.output_dir

    os.makedirs(output_dir, exist_ok=True)

    scrapers = {
        "seatgeek": ("scripts/seatgeek_fetch.py", f"{output_dir}/concerts_seatgeek_{timestamp}.csv"),
        "bandsintown": ("scripts/bandsintown_fetch.py", f"{output_dir}/concerts_bandsintown_{timestamp}.csv"),
        "social": ("scripts/social_scraper.py", f"{output_dir}/social_data_{timestamp}.csv"),
        "streaming": ("scripts/streaming_scraper.py", f"{output_dir}/streaming_data_{timestamp}.csv"),
    }

    print(f"Scraping data for artist: {args.artist}")
    print(f"Output directory: {output_dir}")
    print(f"Sources: {,