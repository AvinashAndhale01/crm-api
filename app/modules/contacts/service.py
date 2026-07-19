from fastapi import HTTPException, status
from app.dependencies.db import SessionDep
from app.modules.contacts.model import Contact
from app.modules.contacts.schema import (
    ContactCreate,
    ContactUpdate,
    PaginatedContactsResponse,
)
from sqlalchemy.orm import Session
from sqlalchemy import or_


def _get_contact_by_id(contact_id: int, session: Session) -> Contact:
    contact = session.get(Contact, contact_id)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


def get_contact(contact_id: int, session: SessionDep) -> Contact:
    return _get_contact_by_id(contact_id, session)


def get_contacts(
    session: SessionDep, limit: int, offset: int
) -> PaginatedContactsResponse:
    contacts = session.query(Contact).limit(limit).offset(offset).all()
    total = session.query(Contact).count()
    return PaginatedContactsResponse(
        total=total,
        limit=limit,
        offset=offset,
        items=contacts,
    )


def create_contact(contact: ContactCreate, session: SessionDep) -> Contact:
    db_contact = Contact(**contact.model_dump())
    session.add(db_contact)
    session.commit()
    session.refresh(db_contact)
    return db_contact


def update_contact(
    contact_id: int, contact: ContactUpdate, session: SessionDep
) -> Contact:
    db_contact = _get_contact_by_id(contact_id, session)
    for key, value in contact.model_dump(exclude_unset=True).items():
        setattr(db_contact, key, value)
    session.commit()
    session.refresh(db_contact)
    return db_contact


def delete_contact(contact_id: int, session: SessionDep) -> dict:
    db_contact = _get_contact_by_id(contact_id, session)
    session.delete(db_contact)
    session.commit()
    return {"detail": "Deleted"}


def search_contacts(
    query: str, limit: int, offset: int, session: SessionDep
) -> PaginatedContactsResponse:
    query = query.strip()
    if not query:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Query cannot be empty"
        )
    search_filter = or_(
        Contact.first_name.ilike(f"%{query}%"),
        Contact.last_name.ilike(f"%{query}%"),
        Contact.email.ilike(f"%{query}%"),
        Contact.phone.ilike(f"%{query}%"),
    )
    contacts = (
        session.query(Contact).filter(search_filter).limit(limit).offset(offset).all()
    )
    total = session.query(Contact).filter(search_filter).count()
    return PaginatedContactsResponse(
        total=total,
        limit=limit,
        offset=offset,
        items=contacts,
    )
