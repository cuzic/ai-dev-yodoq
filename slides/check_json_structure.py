"""
Check structure of measurement results
"""
import json
from pathlib import Path

results_file = Path("/home/cuzic/ai-dev-yodoq/.state/measure/final_results.json")
with open(results_file, "r") as f:
    data = json.load(f)

print("Top-level keys:", list(data.keys()))

if "slides" in data and len(data["slides"]) > 0:
    print("\nFirst slide keys:", list(data["slides"][0].keys()))
    print("\nFirst slide sample:")
    print(json.dumps(data["slides"][0], indent=2))
