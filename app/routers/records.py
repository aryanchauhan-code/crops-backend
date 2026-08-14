from typing import Any
from fastapi import APIRouter, HTTPException, Query
from bson import ObjectId
from bson.errors import InvalidId

from app.database import get_database, DATASET_REGISTRY
from app.models import RecordIn, DatasetInfo, PaginatedRecords

router = APIRouter(prefix="/api", tags=["records"])


def serialize(doc: dict) -> dict:
    """Convert Mongo's ObjectId to a plain string so it's JSON-safe."""
    doc = dict(doc)
    doc["id"] = str(doc.pop("_id"))
    return doc


def to_object_id(record_id: str) -> ObjectId:
    try:
        return ObjectId(record_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail=f"'{record_id}' is not a valid record id")


# ---------- Dataset (collection) discovery ----------

@router.get("/datasets", response_model=list[DatasetInfo])
async def list_datasets():
    """
    Lists every Mongo collection in the database as a 'dataset', enriched with
    friendly metadata from DATASET_REGISTRY where available. This is how the
    frontend builds its sidebar without you hardcoding 17 routes.
    """
    db = get_database()
    collection_names = await db.list_collection_names()
    datasets = []
    for name in sorted(collection_names):
        count = await db[name].count_documents({})
        meta = DATASET_REGISTRY.get(name, {})
        datasets.append(
            DatasetInfo(
                name=name,
                label=meta.get("label", name.replace("_", " ").title()),
                title_field=meta.get("title_field"),
                record_count=count,
            )
        )
    return datasets


# ---------- CRUD over a given dataset/collection ----------

@router.get("/collections/{collection_name}/records", response_model=PaginatedRecords)
async def list_records(
    collection_name: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=5000),
    search: str | None = Query(None, description="Case-insensitive text search across all string fields"),
):
    db = get_database()
    collection = db[collection_name]

    mongo_filter: dict[str, Any] = {}
    if search:
        # Search across every field currently present in the collection's documents.
        sample = await collection.find_one({})
        if sample:
            string_fields = [k for k, v in sample.items() if isinstance(v, str)]
            if string_fields:
                mongo_filter = {
                    "$or": [{field: {"$regex": search, "$options": "i"}} for field in string_fields]
                }

    total = await collection.count_documents(mongo_filter)
    cursor = (
        collection.find(mongo_filter)
        .skip((page - 1) * page_size)
        .limit(page_size)
    )
    items = [serialize(doc) async for doc in cursor]

    return PaginatedRecords(total=total, page=page, page_size=page_size, items=items)


@router.get("/collections/{collection_name}/records/{record_id}")
async def get_record(collection_name: str, record_id: str):
    db = get_database()
    doc = await db[collection_name].find_one({"_id": to_object_id(record_id)})
    if doc is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return serialize(doc)


@router.post("/collections/{collection_name}/records", status_code=201)
async def create_record(collection_name: str, record: RecordIn):
    db = get_database()
    payload = record.model_dump(exclude_unset=True)
    result = await db[collection_name].insert_one(payload)
    doc = await db[collection_name].find_one({"_id": result.inserted_id})
    return serialize(doc)


@router.put("/collections/{collection_name}/records/{record_id}")
async def update_record(collection_name: str, record_id: str, record: RecordIn):
    db = get_database()
    oid = to_object_id(record_id)
    payload = record.model_dump(exclude_unset=True)
    payload.pop("id", None)
    payload.pop("_id", None)

    result = await db[collection_name].update_one({"_id": oid}, {"$set": payload})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Record not found")

    doc = await db[collection_name].find_one({"_id": oid})
    return serialize(doc)


@router.delete("/collections/{collection_name}/records/{record_id}", status_code=204)
async def delete_record(collection_name: str, record_id: str):
    db = get_database()
    result = await db[collection_name].delete_one({"_id": to_object_id(record_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Record not found")
    return None


@router.get("/collections/{collection_name}/fields")
async def get_fields(collection_name: str):
    """
    Returns the union of field names seen across a sample of documents in this
    collection, so the frontend can auto-generate a form/table without you
    hand-coding 70 field definitions per dataset.
    """
    db = get_database()
    fields: list[str] = []
    seen = set()
    async for doc in db[collection_name].find({}).limit(50):
        for key in doc.keys():
            if key != "_id" and key not in seen:
                seen.add(key)
                fields.append(key)
    return {"fields": fields}
