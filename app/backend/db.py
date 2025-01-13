# asPG
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase


engine = create_async_engine('postgresql+asyncpg://ecommerce:Gngff5432@localhost:5432/ecommerce', echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

class Base(DeclarativeBase):
    pass


# sqlite
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, DeclarativeBase
#
# engine = create_engine('sqlite:///ecommerce.db', echo=True)
# SessionLocal = sessionmaker(bind=engine)
# Pg
# engine = create_engine('postgresql+psycopg2://youuser:youpassword@localhost/youdb')
# Dialect+driver://username:password@host:port/database

# asPG
# myusername:mypassword@myhost:5432/mydatabase