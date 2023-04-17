from sqlalchemy.orm import Session
import models, schemas, crypto



# groups
## create
def create_group(db: Session, group=schemas.Group):
    data = models.Group(
        name = group.name,
    )
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

## read
def read_groups(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Group).offset(skip).limit(limit).all()

def read_group_by_id(db: Session, id: int):
    return db.query(models.Group).filter(models.Group.id == id).first()

## update
def update_group_by_id(db: Session, group=schemas.Group):
    db.query(models.Group).filter(models.Group.id == group.id).update({"name": group.name})
    db.commit()
    return db.query(models.Group).filter(models.Group.id == group.id).first()

## delete
def delete_group_by_id(db: Session, id: int):
    db.query(models.Group).filter(models.Group.id == id).delete()
    try:
        db.commit()
    except:
        return False
    return True



# member
## create
def create_member(db: Session, member=schemas.Member):
    data = models.Member(
        gid = member.gid,
        uid = member.uid,
    )
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

## read
def read_member(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Member).offset(skip).limit(limit).all()

def read_member_by_id(db: Session, id: int):
    return db.query(models.Member).filter(models.Member.id == id).first()

def read_member_by_gid(db: Session, gid: int):
    return db.query(models.Member).filter(models.Member.gid == gid).all()

def read_member_by_uid(db: Session, uid: int):
    return db.query(models.Member).filter(models.Member.uid == uid).all()

## update
def update_member_by_id(db: Session, member=schemas.Member):
    db.query(models.Member).filter(models.Member.id == member.id).update({"gid": member.gid, 'uid': member.uid})
    db.commit()
    return db.query(models.Member).filter(models.Member.id == member.id).first()

## delete
def delete_member_by_id(db: Session, id: int):
    db.query(models.Member).filter(models.Member.id == id).delete()
    try:
        db.commit()
    except:
        return False
    return True



# Function
## create
def create_function(db: Session, id: int, name: str):
    data = models.Function(
        id = id,
        name = name
    )
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

## read
def read_function(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Function).offset(skip).limit(limit).all()

def read_function_by_id(db: Session, id: int):
    return db.query(models.Function).filter(models.Function.id == id).first()



# Setting
## create
def create_setting(db: Session, name: str, value: str):
    data = models.Setting(
        name = name,
        value = value
    )
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

## read
def read_setting(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Setting).offset(skip).limit(limit).all()

def read_setting_by_id(db: Session, id: int):
    return db.query(models.Setting).filter(models.Setting.id == id).first()

def read_setting_by_name(db: Session, name: str):
    return db.query(models.Setting).filter(models.Setting.name == name).first()



# role
## create
def create_role(db: Session, role=schemas.Role):
    data = models.Role(
        name = role.name,
        fid = role.fid,
        create = role.create,
        read = role.read,
        update = role.update,
        delete = role.delete
    )
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

## read
def read_role(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Role).offset(skip).limit(limit).all()

def read_role_by_id(db: Session, id: int):
    return db.query(models.Role).filter(models.Role.id == id).first()

def read_role_by_fid(db: Session, fid: int):
    return db.query(models.Role).filter(models.Role.fid == fid).all()

def read_role_by_read(db: Session, read: bool):
    return db.query(models.Role).filter(models.Role.read == read).all()

def read_role_by_write(db: Session, write: bool):
    return db.query(models.Role).filter(models.Role.write == write).all()

## update
def update_role_by_id(db: Session, role=schemas.Role):
    db.query(models.Role).filter(models.Role.id == role.id).update({
        "name": role.name,
        'fid': role.fid,
        'read': role.read,
        'write': role.write
    })
    db.commit()
    return db.query(models.Role).filter(models.Role.id == role.id).first()

## delete
def delete_role_by_id(db: Session, id: int):
    db.query(models.Role).filter(models.Role.id == id).delete()
    try:
        db.commit()
    except:
        return False
    return True



# assign
## create
def create_assign(db: Session, assing=schemas.Assign):
    data = models.Assign(
        rid = assing.rid,
        gid = assing.gid
    )
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

## read
def read_assign(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Assign).offset(skip).limit(limit).all()

def read_assign_by_id(db: Session, id: int):
    return db.query(models.Assign).filter(models.Assign.id == id).first()

def read_assign_by_rid(db: Session, rid: int):
    return db.query(models.Assign).filter(models.Assign.rid == rid).all()

def read_assign_by_fid(db: Session, fid: int):
    return db.query(models.Assign).filter(models.Assign.fid == fid).all()

def read_assign_by_gid(db: Session, gid: int):
    return db.query(models.Assign).filter(models.Assign.gid == gid).all()

def read_assign_by_uid(db: Session, uid: int):
    return db.query(models.Assign).filter(models.Assign.uid == uid).all()

## update
def update_assign_by_id(db: Session, assign=schemas.Assign):
    db.query(models.Assign).filter(models.Assign.id == assign.id).update({
        "rid": assign.rid,
        'fid': assign.fid,
        'gid': assign.gid,
    })
    db.commit()
    return db.query(models.Assign).filter(models.Assign.id == assign.id).first()

## delete
def delete_assign_by_id(db: Session, id: int):
    db.query(models.Assign).filter(models.Assign.id == id).delete()
    try:
        db.commit()
    except:
        return False
    return True



# user
## create
def create_user(db: Session, user=schemas.User):
    public_key = read_setting_by_name(db, "public_key")
    hashed_pwd = crypto.get_hashed_password(user.hash)
    encrypted_pwd = crypto.encrypt(
        bytes(public_key.value, encoding="UTF-8"),
        bytes(hashed_pwd, encoding="UTF-8")
    )

    data = models.User(
        name = user.name,
        hash = encrypted_pwd,
    )
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

## read
def read_user(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def read_user_by_id(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first()

def read_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()

## update
def update_user_by_id(db: Session, user=schemas.User):
    public_key = read_setting_by_name(db, "public_key")
    hashed_pwd = crypto.get_hashed_password(user.hash)
    encrypted_pwd = crypto.encrypt(
        bytes(public_key.value, encoding="UTF-8"),
        bytes(hashed_pwd, encoding="UTF-8")
    )

    db.query(models.User).filter(models.User.id == user.id).update({
        "name": user.name,
        'hash': encrypted_pwd,
    })
    db.commit()
    return db.query(models.User).filter(models.User.id == user.id).first()

## delete
def delete_user_by_id(db: Session, id: int):
    db.query(models.User).filter(models.User.id == id).delete()
    try:
        db.commit()
    except:
        return False
    return True



# secret
## create
def create_secret(db: Session, secret=schemas.Secret):
    data = models.Secret(
        name = secret.name,
        value = secret.value,
        sse = secret.sse
    )
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

## read
def read_secret(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Secret).offset(skip).limit(limit).all()

def read_secret_by_id(db: Session, id: int):
    return db.query(models.Secret).filter(models.Secret.id == id).first()

def read_secret_by_name(db: Session, name: str):
    return db.query(models.Secret).filter(models.Secret.name == name).first()

## update
def update_secret_by_id(db: Session, secret=schemas.Secret):
    db.query(models.Secret).filter(models.Secret.id == secret.id).update({
        "name": secret.name,
        'value': secret.value,
        'sse': secret.sse
    })
    db.commit()
    return db.query(models.Secret).filter(models.Secret.id == secret.id).first()

## delete
def delete_secret_by_id(db: Session, id: int):
    db.query(models.Secret).filter(models.Secret.id == id).delete()
    try:
        db.commit()
    except:
        return False
    return True
