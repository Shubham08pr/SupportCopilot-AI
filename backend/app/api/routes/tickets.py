from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.app.services.ticket_service import (
    create_ticket,
    get_all_tickets,
    get_ticket,
    update_ticket_response
)

from backend.app.services.retrieval_service import retrieve_chunks, compute_confidence
from backend.app.services.llm_service import generate_response

router = APIRouter()


class TicketRequest(BaseModel):
    query: str


@router.post("/tickets")
def create(req: TicketRequest):
    return create_ticket(req.query)


@router.get("/tickets")
def list_tickets():
    return get_all_tickets()


@router.post("/tickets/{ticket_id}/suggest-response")
def suggest(ticket_id: int):
    ticket = get_ticket(ticket_id)

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    results = retrieve_chunks(ticket["query"])
    confidence = compute_confidence(results)

    context = "\n\n".join([r["text"] for r in results])
    response = generate_response(ticket["query"], context)

    update_ticket_response(ticket_id, response)

    decision = "auto-response" if confidence >= 0.75 else "needs-agent"

    return {
        "ticket_id": ticket_id,
        "suggested_response": response,
        "confidence": confidence,
        "decision": decision
    }