tickets_db = []
ticket_id_counter = 1


def create_ticket(query: str):
    global ticket_id_counter

    ticket = {
        "id": ticket_id_counter,
        "query": query,
        "status": "open",
        "ai_response": None
    }

    tickets_db.append(ticket)
    ticket_id_counter += 1

    return ticket


def get_all_tickets():
    return tickets_db


def get_ticket(ticket_id: int):
    for t in tickets_db:
        if t["id"] == ticket_id:
            return t
    return None


def update_ticket_response(ticket_id: int, response: str):
    ticket = get_ticket(ticket_id)
    if ticket:
        ticket["ai_response"] = response
    return ticket