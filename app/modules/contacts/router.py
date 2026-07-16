from fastapi import APIRouter, status, Query
from app.dependencies.db import SessionDep
from app.modules.contacts import service
from app.modules.contacts.schema import (
    ContactCreate,
    ContactResponse,
    ContactUpdate,
    PaginatedContactsResponse,
)


router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/search/", response_model=list[ContactResponse])
async def search_contacts(query: str, session: SessionDep):
    return service.search_contacts(query, session)


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int, session: SessionDep):
    return service.get_contact(contact_id, session)


@router.get("/", response_model=PaginatedContactsResponse)
async def get_contacts(
    session: SessionDep,
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    return service.get_contacts(session, limit=limit, offset=offset)


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(contact: ContactCreate, session: SessionDep):
    return service.create_contact(contact, session)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(contact_id: int, contact: ContactUpdate, session: SessionDep):
    return service.update_contact(contact_id, contact, session)


@router.delete("/{contact_id}", status_code=status.HTTP_200_OK)
async def delete_contact(contact_id: int, session: SessionDep):
    return service.delete_contact(contact_id, session)
