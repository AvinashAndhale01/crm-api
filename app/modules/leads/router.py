from fastapi import APIRouter, status, Query
from app.dependencies.db import SessionDep
from app.modules.leads.schema import (
    LeadResponse,
    LeadCreate,
    LeadUpdate,
    MessageResponse,
    PaginatedLeadResponse,
)
from app.modules.leads import service


router = APIRouter(prefix="/leads", tags=["leads"])


@router.get("/{lead_id}", response_model=LeadResponse)
def get_lead(lead_id: int, session: SessionDep):
    db_lead = service.get_lead(lead_id, session)
    return db_lead


@router.get("/", response_model=PaginatedLeadResponse)
def get_leads(
    session: SessionDep,
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    return service.get_leads(session, limit, offset)


@router.post("/", response_model=LeadResponse, status_code=status.HTTP_201_CREATED)
def create_lead(lead: LeadCreate, session: SessionDep):
    new_lead = service.create_lead(lead, session)
    return new_lead


@router.put("/{lead_id}", response_model=LeadResponse)
def update_lead(lead_id: int, lead: LeadUpdate, session: SessionDep):
    existing_lead = service.update_lead(lead_id, lead, session)
    return existing_lead


@router.delete(
    "/{lead_id}", response_model=MessageResponse, status_code=status.HTTP_200_OK
)
def delete_lead(lead_id: int, session: SessionDep):
    return service.delete_lead(lead_id, session)
