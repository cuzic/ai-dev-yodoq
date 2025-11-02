"""
Re-measure slides after fixes to see improvements
"""
import asyncio
import json
from pathlib import Path
import sys

# Import the measurement function from the original script
sys.path.insert(0, str(Path(__file__).parent))
from measure_marp_quality import measure_slides, save_results, print_summary

async def main():
    html_file = Path("/home/cuzic/ai-dev-yodoq/render/slides.html")
    output_file = Path("/home/cuzic/ai-dev-yodoq/.state/measure/final_results.json")

    print("Re-measuring slides after fixes...")
    results = await measure_slides(html_file)

    print("Saving results...")
    save_results(results, output_file)

    print_summary(results)

    print(f"\nResults saved to: {output_file}")

if __name__ == "__main__":
    asyncio.run(main())
