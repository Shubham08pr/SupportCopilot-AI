from fastapi import APIRouter
from pydantic import BaseModel
import time

from backend.app.services.logging_service import log_request
from backend.app.services.retrieval_service import retrieve_chunks, compute_confidence, compute_retrieval_confidence
from backend.app.services.llm_service import evaluate_response, generate_response
from backend.app.services.routing_service import decide_action

router = APIRouter()


class QueryRequest(BaseModel):
    query: str


@router.post("/query")
def query(req: QueryRequest):

    start_time = time.time()

    if not req.query.strip():
        return {"answer": "Query cannot be empty"}

    results = retrieve_chunks(req.query)

    if not results:

        latency_ms = int((time.time() - start_time) * 1000)

        log_request({
            "query": req.query,
            "answer": "No relevant data found",
            "retrieval_confidence": 0.0,
            "llm_confidence": 0.0,
            "final_confidence": 0.0,
            "action": "ESCALATE",
            "latency_ms": latency_ms
        })

        return {
            "answer": "No relevant data found",
            "retrieval_confidence": 0.0,
            "llm_confidence": 0.0,
            "final_confidence": 0.0,
            "action": "ESCALATE",
            "sources": []
        }

    retrieval_confidence = compute_retrieval_confidence(results)

    context = "\n\n".join([r["text"] for r in results[:2]])

    answer = generate_response(req.query, context)

    llm_confidence = evaluate_response(
        req.query,
        answer,
        context
    )

    final_confidence = compute_confidence(
        retrieval_confidence,
        llm_confidence
    )

    action = decide_action(final_confidence)

    latency_ms = int((time.time() - start_time) * 1000)

    log_request({
        "query": req.query,
        "answer": answer,
        "retrieval_confidence": retrieval_confidence,
        "llm_confidence": llm_confidence,
        "final_confidence": final_confidence,
        "action": action,
        "latency_ms": latency_ms
    })

    return {
        "answer": answer,
        "retrieval_confidence": retrieval_confidence,
        "llm_confidence": llm_confidence,
        "final_confidence": final_confidence,
        "action": action,
        "sources": [r["metadata"] for r in results]
    }