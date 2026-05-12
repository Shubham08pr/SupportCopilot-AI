from fastapi import FastAPI

from backend.app.api.routes.query import router as query_router
from backend.app.api.routes.search import router as search_router
from backend.app.api.routes.tickets import router as ticket_router
from backend.app.api.routes.health import router as health_router

app = FastAPI()

app.include_router(query_router)
app.include_router(search_router)
app.include_router(ticket_router)
app.include_router(health_router)