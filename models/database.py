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
