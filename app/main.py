import meilisearch
import logging
import os
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO)

# --- Configuration ---
# In a real application, these would come from a config file or environment variables
MEILI_URL = os.environ.get("MEILI_URL", "http://127.0.0.1:7700")
MEILI_MASTER_KEY = os.environ.get("MEILI_MASTER_KEY", None) # Set this in your environment
SAVE_TO_MEILISEARCH = True

MusicEvent = Dict[str, Any]

def save_to_meilisearch(events: List[MusicEvent]):
    """Saves the list of events to a MeiliSearch instance."""
    if not SAVE_TO_MEILISEARCH:
        logging.info("Skipping save to MeiliSearch (feature flag is off).")
        return

    logging.info(f"Saving {len(events)} events to MeiliSearch at {MEILI_URL}")
    try:
        client = meilisearch.Client(MEILI_URL, MEILI_MASTER_KEY)
        index = client.index("events")
        index.add_documents(events, primary_key='id')
    except Exception as e:
        logging.error(f"Failed to save events to MeiliSearch: {e}")

def search_events(query: str, search_fields: List[str] = None):
    """Searches for events in MeiliSearch."""
    client = meilisearch.Client(MEILI_URL, MEILI_MASTER_KEY)
    index = client.index("events")
    
    search_params = {}
    if search_fields:
        search_params['attributesToSearchOn'] = search_fields

    return index.search(query, search_params)

if __name__ == '__main__':
    # --- Example Usage ---
    sample_events = [
      {
        "id": "19hz-85",
        "name": "Hawthorn Feat. Clee + Label, Mon, Espi, Szymkowski",
        "artists": [
          "Hawthorn",
          "Clee + Label",
          "Mon",
          "Espi",
          "Szymkowski"
        ],
        "venue": "Hawthorn",
        "city": "San Francisco",
        "country": "United States",
        "date": "2025-08-01T07:24:44.615780+00:00"
      },
      {
        "id": "rgr-123",
        "name": "Another Event",
        "artists": ["Some Artist", "Another Artist"],
        "venue": "Some Venue",
        "city": "New York",
        "country": "United States",
        "date": "2024-10-15T20:00:00.000000+00:00"
      }
    ]

    # You will need to set the MEILI_URL and MEILI_MASTER_KEY environment variables
    # For example:
    # export MEILI_URL="http://YOUR_EC2_IP:7700"
    # export MEILI_MASTER_KEY="your_meili_master_key"

    if MEILI_URL == "http://127.0.0.1:7700":
        logging.warning("MEILI_URL is not set. Using default http://127.0.0.1:7700")

    save_to_meilisearch(sample_events)

    # Example searches
    print("Searching for 'Hawthorn':")
    results = search_events("Hawthorn")
    print(results)

    print("\nSearching for 'New York' in city and venue:")
    results_ny = search_events("New York", search_fields=['city', 'venue'])
    print(results_ny) 