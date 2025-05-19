import aiohttp
import json
import os
from datetime import datetime, timedelta

async def fetch_federal_data():
    today = datetime.utcnow().date()
    start_date = (today - timedelta(days=7)).isoformat()

    url = f"https://www.federalregister.gov/api/v1/documents.json?conditions[publication_date][gte]={start_date}&order=newest"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    print(f"Failed to fetch data. Status code: {resp.status}")
                    return

                data = await resp.json()
                results = data.get("results", [])
                print(f"Fetched {len(results)} documents.")

                # Ensure the folder exists
                os.makedirs("pipeline", exist_ok=True)

                with open("pipeline/raw_data.json", "w", encoding="utf-8") as f:
                    json.dump(results, f, ensure_ascii=False, indent=2)

                print("Saved to pipeline/raw_data.json ✅")

    except Exception as e:
        print(f"Error during fetch: {e}")

# Entry point
if __name__ == "__main__":
    import asyncio
    asyncio.run(fetch_federal_data())
