from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.sql import func
from sqlalchemy import DateTime, Text
from datetime import datetime

engine = create_async_engine(url = "sqlite+aiosqlite:///db.sqlite3")

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key = True)
    tg_id = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(100), nullable = False)
    phone: Mapped[str] = mapped_column(String(20), nullable = False)
    username: Mapped[str] = mapped_column(String(50), nullable = False)

class OrderDescription(Base):
    __tablename__ = "descriptions"
    id: Mapped[int] = mapped_column(primary_key = True)
    user: Mapped[int] = mapped_column(ForeignKey("users.id"))
    category: Mapped[str] = mapped_column(String(50))  
    package: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    city: Mapped[str] = mapped_column(String(50), nullable=False)
    package_code: Mapped[str] = mapped_column(String(50))

class Broadcast(Base):
    __tablename__ = "broadcasts"
    id: Mapped[int] = mapped_column(primary_key = True)
    message: Mapped[str] = mapped_column(String, nullable = False)

class PackagePrice(Base):
    __tablename__ = "package_prices"
 
    id: Mapped[int] = mapped_column(primary_key=True)
    package_name: Mapped[str] = mapped_column(String(50), nullable=False)  
    city: Mapped[str] = mapped_column(String(50), nullable=False)          
    price: Mapped[str] = mapped_column(String(50), nullable=False)

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)