from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Identity, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from database import Base

'''
nomenclature:

gid = group id
mid = memeber id
fid = function id
rid = role id
aid = assign id
uid = user id
sid = secret id

group
|id:int:pk:index:auto|name:string:index   |modified:timestamp  |
|--------------------|--------------------|--------------------|
|1                   |admin               |1-1-2023 00:00:00:00|
|2                   |group-1             |1-1-2023 00:00:00:00|
|3                   |group-2             |1-1-2023 00:00:00:00|
|4                   |group-3             |1-1-2023 00:00:00:00|
'''
class Group(Base):
    __tablename__ = "group"
    id = Column(Integer, Identity(start=0, cycle=True), primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    member = relationship("Member")
    modified = Column(DateTime(timezone=True), onupdate=func.now())
    created = Column(DateTime(timezone=True), server_default=func.now())

'''
member
|id:int:pk:index:auto|gid:int:fk:index    |uid:int:fk:index    |modified:timestamp  |
|--------------------|--------------------|--------------------|--------------------|
|1                   |1                   |1                   |1-1-2023 00:00:00:00|
|2                   |2                   |2                   |1-1-2023 00:00:00:00|
|3                   |3                   |2                   |1-1-2023 00:00:00:00|
|4                   |4                   |2                   |1-1-2023 00:00:00:00|
'''
class Member(Base):
    __tablename__ = "member"
    id = Column(Integer, Identity(start=0, cycle=True), primary_key=True, index=True,)
    gid = Column(Integer, ForeignKey("group.id"), index=True, nullable=False,)
    group = relationship("Group", viewonly=True)
    uid = Column(Integer, ForeignKey("user.id"), index=True, nullable=False,)
    user = relationship("User", viewonly=True)
    modified = Column(DateTime(timezone=True), onupdate=func.now())
    created = Column(DateTime(timezone=True), server_default=func.now())
'''
function
|id:int:pk:index:auto|name:string:index   |modified:timestamp  |
|--------------------|--------------------|--------------------|
|1                   |group               |1-1-2023 00:00:00:00|
|2                   |member              |1-1-2023 00:00:00:00|
|4                   |role                |1-1-2023 00:00:00:00|
|5                   |assign              |1-1-2023 00:00:00:00|
|6                   |user                |1-1-2023 00:00:00:00|
|7                   |secret              |1-1-2023 00:00:00:00|
'''
class Function(Base):
    __tablename__ = "function"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    modified = Column(DateTime(timezone=True), onupdate=func.now())
    created = Column(DateTime(timezone=True), server_default=func.now())


'''
role
|id:int:pk:index:auto|name:string:index   |fid:int:fk          |read:bool           |write:bool          |modified:timestamp |
|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|
|1                   |rw-group            |1                   |true                |true                |1-1-2023 00:00:00:00|
|2                   |r-group             |1                   |true                |false               |1-1-2023 00:00:00:00|
|3                   |w-group             |1                   |false               |false               |1-1-2023 00:00:00:00|
'''
class Role(Base):
    __tablename__ = "role"
    id = Column(Integer, Identity(start=0, cycle=True),primary_key=True, index=True, )
    name = Column(String, index=True, unique=True)
    fid = Column(Integer, ForeignKey("function.id") , index=True, )
    read = Column(Boolean)
    write = Column(Boolean)
    modified = Column(DateTime(timezone=True), onupdate=func.now())
    created = Column(DateTime(timezone=True), server_default=func.now())


'''
assign
|id:int:pk:index:auto|rid:int:fk          |gid:int:fk          |modified:timestamp  |
|--------------------|--------------------|--------------------|--------------------|
|1                   |1                   |1                   |1-1-2023 00:00:00:00|
|2                   |2                   |2                   |1-1-2023 00:00:00:00|
|3                   |3                   |3                   |1-1-2023 00:00:00:00|
'''
class Assign(Base):
    __tablename__ = "assign"
    id = Column(Integer, Identity(start=0, cycle=True),primary_key=True, index=True, )
    rid = Column(Integer, ForeignKey("role.id"))
    gid = Column(Integer, ForeignKey("group.id"))
    modified = Column(DateTime(timezone=True), onupdate=func.now())
    created = Column(DateTime(timezone=True), server_default=func.now())


'''
user
|id:int:pk:index:auto|name:string:index   |hash:string         |modified:timestamp  |
|--------------------|--------------------|--------------------|--------------------|
|1                   |admin-pwd           |base64 rsa encrypted|1-1-2023 00:00:00:00|
|2                   |my-secret-1-user-1  |base64 rsa encrypted|1-1-2023 00:00:00:00|
|3                   |my-secret-2-user-1  |base64 rsa encrypted|1-1-2023 00:00:00:00|
|4                   |my-secret-3-user-1  |base64 rsa encrypted|1-1-2023 00:00:00:00|
'''
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, Identity(start=0, cycle=True),primary_key=True, index=True, )
    name = Column(String, index=True, unique=True)
    hash = Column(String)
    member = relationship("Member", viewonly=True)
    modified = Column(DateTime(timezone=True), onupdate=func.now())
    created = Column(DateTime(timezone=True), server_default=func.now())


'''
setting
|id:int:pk:index:auto|name:string:index   |value:string        |modified:timestamp  |
|--------------------|--------------------|--------------------|--------------------|
|1                   |admin-pwd           |base64 rsa encrypted|1-1-2023 00:00:00:00|
|2                   |my-secret-1-user-1  |base64 rsa encrypted|1-1-2023 00:00:00:00|
|3                   |my-secret-2-user-1  |base64 rsa encrypted|1-1-2023 00:00:00:00|
|4                   |my-secret-3-user-1  |base64 rsa encrypted|1-1-2023 00:00:00:00|
'''
class Setting(Base):
    __tablename__ = "setting"
    id = Column(Integer, Identity(start=0, cycle=True),primary_key=True, index=True, )
    name = Column(String, index=True, unique=True)
    value = Column(String)
    modified = Column(DateTime(timezone=True), onupdate=func.now())
    created = Column(DateTime(timezone=True), server_default=func.now())



'''
secret
|id:int:pk:index:auto|name:string:index   |value:string        |modified:timestamp  |
|--------------------|--------------------|--------------------|--------------------|
|1                   |admin-pwd           |base64 rsa encrypted|1-1-2023 00:00:00:00|
|2                   |my-secret-1-user-1  |base64 rsa encrypted|1-1-2023 00:00:00:00|
|3                   |my-secret-2-user-1  |base64 rsa encrypted|1-1-2023 00:00:00:00|
|4                   |my-secret-3-user-1  |base64 rsa encrypted|1-1-2023 00:00:00:00|
'''
class Secret(Base):
    __tablename__ = "secret"
    id = Column(Integer, Identity(start=0, cycle=True),primary_key=True, index=True, )
    name = Column(String, index=True, unique=True)
    value = Column(String)
    sse = Column(Boolean)
    modified = Column(DateTime(timezone=True), onupdate=func.now())
    created = Column(DateTime(timezone=True), server_default=func.now())
