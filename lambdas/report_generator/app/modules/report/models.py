
import uuid
from datetime import date, datetime

from sqlalchemy import (
    BigInteger,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class DailyReport(Base):
    __tablename__ = "daily_reports"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "report_date",
            name="uq_daily_report_user_date",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    report_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    total_files: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    total_storage_bytes: Mapped[int] = mapped_column(
        BigInteger,
        default=0,
        nullable=False,
    )

    uploads_today: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    bytes_uploaded_today: Mapped[int] = mapped_column(
        BigInteger,
        default=0,
        nullable=False,
    )

    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
