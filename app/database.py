from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

_client: AsyncIOMotorClient | None = None


def get_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(settings.mongodb_uri)
    return _client


def get_database():
    return get_client()[settings.mongodb_db_name]


async def close_client():
    global _client
    if _client is not None:
        _client.close()
        _client = None


# Collections we consider "known datasets" get registered here with a friendly
# display name + which field to use as the human-readable title in the UI.
# Add an entry per CSV file you import (17 files -> 17 entries eventually).
# This is metadata only -- it does NOT restrict which collections exist in Mongo,
# it just helps the frontend show nice labels and pick a sensible "title field".
DATASET_REGISTRY: dict[str, dict] = {
    "fermented_beverages": {
        "label": "Traditional Fermented Beverages",
        "title_field": "Beverage Name",
    },
    # "crops_by_state": {
    #     "label": "Crops by State",
    #     "title_field": "Crop Name",
    # },
    # ... add one entry per additional file as you import it
}
