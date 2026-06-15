from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class Followup(TimestampMixin, Base):
    __tablename__ = "followups"

    id: Mapped[int] = mapped_column(primary_key=True)

    lead_id: Mapped[int] = mapped_column(
        ForeignKey("leads.id", ondelete="CASCADE"), nullable=False, index=True
    )

    step_1: Mapped[bool] = mapped_column(Boolean, default=False)
    step_2: Mapped[bool] = mapped_column(Boolean, default=False)
    step_3: Mapped[bool] = mapped_column(Boolean, default=False)
    step_4: Mapped[bool] = mapped_column(Boolean, default=False)
    step_5: Mapped[bool] = mapped_column(Boolean, default=False)
    step_6: Mapped[bool] = mapped_column(Boolean, default=False)
    step_7: Mapped[bool] = mapped_column(Boolean, default=False)

    lead: Mapped["Lead"] = relationship("Lead", back_populates="followups")
