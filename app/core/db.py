from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.core.config import settings

engine_master = create_async_engine(settings.DATABASE_URL_MASTER)
engine_replica = create_async_engine(settings.DATABASE_URL_REPLICA)
SessionLocalMaster = async_sessionmaker(bind=engine_master, expire_on_commit=False)
SessionLocalReplica = async_sessionmaker(bind=engine_replica, expire_on_commit=False)
Base = declarative_base()


async def get_db_replica():
    async with SessionLocalReplica() as db:
        print("replica")
        yield db


async def get_db_master():
    async with SessionLocalMaster() as db:
        print("master")
        yield db
