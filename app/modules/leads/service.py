from fastapi import HTTPException, status
from app.db.models import Lead
from app.modules.leads.schema import (
    LeadResponse,
    LeadCreate,
    LeadUpdate,
    MessageResponse,
    PaginatedLeadResponse,
)
from app.core.enums import LeadStatus, LeadSource
from sqlalchemy.orm import Session


OPEN_LEAD_EXCLUDED_STATUSES = (
    LeadStatus.WON,
    LeadStatus.LOST,
)


def _get_lead_by_id(lead_id: int, session: Session) -> Lead:
    lead = session.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found"
        )
    return lead


def _find_open_lead(
    session: Session,
    contact_id: int,
    source: LeadSource,
    exclude_lead_id: int | None = None,
) -> Lead | None:
    query = session.query(Lead).filter(
        Lead.contact_id == contact_id,
        Lead.source == source,
        Lead.status.notin_(OPEN_LEAD_EXCLUDED_STATUSES),
    )
    if exclude_lead_id is not None:
        query = query.filter(Lead.id != exclude_lead_id)
    return query.first()


def get_lead(lead_id: int, session: Session) -> LeadResponse:
    return _get_lead_by_id(lead_id, session)


def get_leads(session: Session, limit: int, offset: int) -> PaginatedLeadResponse:
    total = session.query(Lead).count()

    leads = (
        session.query(Lead)
        .order_by(Lead.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return PaginatedLeadResponse(
        total=total,
        limit=limit,
        offset=offset,
        items=leads,
    )


def create_lead(lead: LeadCreate, session: Session) -> LeadResponse:
    existing_lead = _find_open_lead(
        session=session,
        contact_id=lead.contact_id,
        source=lead.source,
    )
    if existing_lead:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An open lead with the same source already exists for this contact.",
        )

    db_lead = Lead(**lead.model_dump())
    session.add(db_lead)
    session.commit()
    session.refresh(db_lead)
    return db_lead


def update_lead(lead_id: int, lead: LeadUpdate, session: Session) -> LeadResponse:
    existing_lead = _get_lead_by_id(lead_id, session)
    source = lead.source if lead.source is not None else existing_lead.source
    duplicate = _find_open_lead(
        session=session,
        contact_id=existing_lead.contact_id,
        source=source,
        exclude_lead_id=lead_id,
    )

    if duplicate:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An open lead with the same source already exists for this contact.",
        )

    for key, value in lead.model_dump(exclude_unset=True).items():
        setattr(existing_lead, key, value)
    session.commit()
    session.refresh(existing_lead)
    return existing_lead


def delete_lead(lead_id: int, session: Session) -> MessageResponse:
    existing_lead = _get_lead_by_id(lead_id, session)
    session.delete(existing_lead)
    session.commit()
    return MessageResponse(detail="Lead deleted successfully")
