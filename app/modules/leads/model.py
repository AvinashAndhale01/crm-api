from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, Enum, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import LeadSource, LeadStatus
from app.db.base import Base, TimestampMixin


if TYPE_CHECKING:
    from app.modules.contacts.model import Contact
    from app.modules.followups.model import Followup
    from app.modules.notes.model import Note
    from app.modules.users.model import User


class Lead(TimestampMixin, Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[LeadStatus] = mapped_column(
        Enum(LeadStatus), default=LeadStatus.INITIAL_CONTACT, nullable=False
    )
    source: Mapped[LeadSource] = mapped_column(Enum(LeadSource), nullable=False)
    value: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    last_contact_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    next_contact_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    contact_id: Mapped[int] = mapped_column(
        ForeignKey("contacts.id", ondelete="RESTRICT"), nullable=False
    )
    assigned_to_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    # Customer associated with this lead
    contact: Mapped["Contact"] = relationship("Contact", back_populates="leads")

    # Salesperson responsible
    assigned_to: Mapped["User"] = relationship("User", back_populates="leads")
    followups: Mapped[list["Followup"]] = relationship(
        "Followup", back_populates="lead", cascade="all, delete-orphan"
    )

    # Lead notes
    notes: Mapped[list["Note"]] = relationship(
        "Note", back_populates="lead", cascade="all, delete-orphan"
    )
