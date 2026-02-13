from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Float, DateTime, func
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# SQLAlchemy Setup
DATABASE_URL = "sqlite+aiosqlite:///./accounting.db"
engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class Invoice(Base):
    __tablename__ = "invoices"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    invoice_id: Mapped[str] = mapped_column(String, unique=True)
    vendor: Mapped[str] = mapped_column(String)
    amount: Mapped[float] = mapped_column(Float)
    date: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String, default="Pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    
    # New fields for rich metadata
    due_date: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    payment_terms: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    po_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    department: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    subtotal: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    tax_rate: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    tax_amount: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    approval_status: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(String, nullable=True)

# Pydantic Schemas
class InvoiceSchema(BaseModel):
    invoice_id: str
    vendor: str
    amount: float
    date: str
    status: str = "Pending"

    class Config:
        from_attributes = True

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
