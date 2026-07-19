from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from decimal import Decimal
from app.core.enums import LeadSource, LeadStatus


class LeadBase(BaseModel):
    status: LeadStatus | None = None
    source: LeadSource | None = None
    value: Decimal | None = Field(default=None, ge=0)


class LeadCreate(LeadBase):
    contact_id: int
    assigned_to_id: int | None = None


class LeadUpdate(LeadBase):
    last_contact_at: datetime | None = None
    next_contact_at: datetime | None = None
    assigned_to_id: int | None = None


class LeadResponse(LeadBase):
    id: int
    last_contact_at: datetime | None = None
    next_contact_at: datetime | None = None
    contact_id: int
    assigned_to_id: int | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MessageResponse(BaseModel):
    detail: str


class PaginatedLeadResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[LeadResponse]
