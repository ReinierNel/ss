from pydantic import BaseModel
import datetime

class Group(BaseModel):
    id: int | None = 0
    name: str
    modified: datetime.datetime | None = None
    created: datetime.datetime | None = None

class Member(BaseModel):
    id: int | None = None
    gid: int
    uid: int
    modified: datetime.datetime | None = None
    created: datetime.datetime | None = None

class Function(BaseModel):
    id: int | None = None
    name: str
    modified: datetime.datetime | None = None
    created: datetime.datetime | None = None

class Role(BaseModel):
    id: int | None = None
    name: str
    fid: int
    read: bool
    write: bool
    modified: datetime.datetime | None = None
    created: datetime.datetime | None = None

class Assign(BaseModel):
    id: int | None = None
    rid: int
    gid: int
    modified: datetime.datetime | None = None
    created: datetime.datetime | None = None

class User(BaseModel):
    id: int | None = None
    name: str
    hash: str
    modified: datetime.datetime | None = None
    created: datetime.datetime | None = None

class Setting(BaseModel):
    id: int | None = None
    name: str
    value: str
    modified: datetime.datetime | None = None
    created: datetime.datetime | None = None

class Secret(BaseModel):
    id: int | None = None
    name: str
    value: str
    sse: bool | None = None
    modified: datetime.datetime | None = None
    created: datetime.datetime | None = None
