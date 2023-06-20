from uuid import UUID

from sqlmodel import SQLModel, Field


class SQLPackage(SQLModel, table=True):
    uuid: UUID = Field(default=None, primary_key=True)
    name: str = Field(sa_column_kwargs={"unique": True})

    class Config:
        orm_mode = True
