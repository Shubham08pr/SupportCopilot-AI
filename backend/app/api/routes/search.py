from fastapi import APIRouter
from pydantic import BaseModel
from backend.app.services.retrieval_service import retrieve_chunks

router = APIRouter()


class SearchRequest(BaseModel):
    query: str


@router.post("/search")
def search(req: SearchRequest):
    results = retrieve_chunks(req.query)

    return {
        "results": results
    }