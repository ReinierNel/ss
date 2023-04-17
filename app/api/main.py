from fastapi import Depends, FastAPI, HTTPException, status, Header
from sqlalchemy.orm import Session

import crud, models, schemas, default, crypto, rbac
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

# init defailts
default.init()

app = FastAPI(
    title="SS API",
    description="SS or Simple Secrets",
    version="v0.0.2",
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_rbac(function_id: int, db: Session, api_user: str, api_password: str, create = False, read = False, update = False, delete = False):

    if not rbac.check_user(db, api_user, api_password):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    if not rbac.check_rbac(db, api_user, function_id, create, read, update, delete):
        raise HTTPException(status_code=403, detail="Forbidden")

# Group
@app.post("/group/", status_code=status.HTTP_201_CREATED, tags=["Group"])
def create_group(
        group: schemas.Group,
        db: Session = Depends(get_db),
        api_user: str | None = Header(default=None, convert_underscores=True),
        api_password: str | None = Header(default=None, convert_underscores=True),
    ):

    get_rbac(
        function_id=0,
        db=db,
        api_user=api_user,
        api_password=api_password,
        create=True
    )

    return crud.create_group(db, group)

@app.get("/group/", status_code=status.HTTP_200_OK, tags=["Group"])
def read_groups(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db),
        api_user: str | None = Header(default=None, convert_underscores=True),
        api_password: str | None = Header(default=None, convert_underscores=True),
    ):
    
    get_rbac(
        function_id=0,
        db=db,
        api_user=api_user,
        api_password=api_password,
        read=True
    )

    return crud.read_groups(db, skip, limit)

@app.get("/group/{id}", status_code=status.HTTP_200_OK, tags=["Group"], response_model=schemas.Group)
def read_group_by_id(
        id: int,
        db: Session = Depends(get_db),
        api_user: str | None = Header(default=None, convert_underscores=True),
        api_password: str | None = Header(default=None, convert_underscores=True),
    ):
    
    get_rbac(
        function_id=0,
        db=db,
        api_user=api_user,
        api_password=api_password,
        read=True
    )
    
    fetch = crud.read_group_by_id(db, id)
    return fetch.__dict__

@app.put("/group/", status_code=status.HTTP_201_CREATED, tags=["Group"], response_model=schemas.Group)
def update_group_by_id(
        group: schemas.Group,
        db: Session = Depends(get_db),
        api_user: str | None = Header(default=None, convert_underscores=True),
        api_password: str | None = Header(default=None, convert_underscores=True),
    ):
    
    get_rbac(
        function_id=0,
        db=db,
        api_user=api_user,
        api_password=api_password,
        update=True
    )
    
    update = crud.update_group_by_id(db, group)
    return update.__dict__

@app.delete("/group/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["Group"])
def delete_group_by_id(
        id: int,
        db: Session = Depends(get_db),
        api_user: str | None = Header(default=None, convert_underscores=True),
        api_password: str | None = Header(default=None, convert_underscores=True),
    ):
    
    get_rbac(
        function_id=0,
        db=db,
        api_user=api_user,
        api_password=api_password,
        delete=True
    )
    
    if crud.delete_group_by_id(db, id):
        return {'detail': 'deleted'}
    else:
        raise HTTPException(status_code=500, detail="failed deletion")





# Member
@app.post("/member/", status_code=status.HTTP_201_CREATED, tags=["Member"])
def create_member(
        member: schemas.Member,
        db: Session = Depends(get_db),
        api_user: str | None = Header(default=None, convert_underscores=True),
        api_password: str | None = Header(default=None, convert_underscores=True),
    ):
    
    get_rbac(
        function_id=1,
        db=db,
        api_user=api_user,
        api_password=api_password,
        create=True
    )
    
    return crud.create_member(db, member)

@app.get("/member/", status_code=status.HTTP_200_OK, tags=["Member"])
def read_member(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db),
        api_user: str | None = Header(default=None, convert_underscores=True),
        api_password: str | None = Header(default=None, convert_underscores=True),
    ):
    
    get_rbac(
        function_id=1,
        db=db,
        api_user=api_user,
        api_password=api_password,
        read=True
    )
    
    return crud.read_member(db, skip, limit)

@app.get("/member/{id}", status_code=status.HTTP_200_OK, tags=["Member"], response_model=schemas.Member)
def read_member_by_id(
        id: int,
        db: Session = Depends(get_db),
        api_user: str | None = Header(default=None, convert_underscores=True),
        api_password: str | None = Header(default=None, convert_underscores=True),
    ):
    
    get_rbac(
        function_id=1,
        db=db,
        api_user=api_user,
        api_password=api_password,
        read=True
    )
    
    fetch = crud.read_member_by_id(db, id)
    fetch.__dict__
    return fetch.__dict__

@app.put("/member/", status_code=status.HTTP_201_CREATED, tags=["Member"], response_model=schemas.Member)
def update_member_by_id(
        member: schemas.Member,
        db: Session = Depends(get_db),
        api_user: str | None = Header(default=None, convert_underscores=True),
        api_password: str | None = Header(default=None, convert_underscores=True),
    ):
    
    get_rbac(
        function_id=1,
        db=db,
        api_user=api_user,
        api_password=api_password,
        update=True
    )
    
    update = crud.update_member_by_id(db, member)
    return update.__dict__

@app.delete("/member/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["Member"])
def delete_member_by_id(
        id: int,
        db: Session = Depends(get_db),
        api_user: str | None = Header(default=None, convert_underscores=True),
        api_password: str | None = Header(default=None, convert_underscores=True),
    ):
    
    get_rbac(
        function_id=1,
        db=db,
        api_user=api_user,
        api_password=api_password,
        delete=True
    )
    
    if crud.delete_member_by_id(db, id):
        return {'detail': 'deleted'}
    else:
        raise HTTPException(status_code=500, detail="failed deletion")




# Function
@app.get("/function/", status_code=status.HTTP_200_OK, tags=["Function"])
def read_function(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db),
    ):
    return crud.read_function(db, skip, limit)

@app.get("/function/{id}", status_code=status.HTTP_200_OK, tags=["Function"], response_model=schemas.Function)
def read_function_by_id(
        id: int,
        db: Session = Depends(get_db),
    ):
    fetch = crud.read_function_by_id(db, id)
    return fetch.__dict__




# Setting
@app.get("/setting/key/public", status_code=status.HTTP_200_OK, tags=["Setting"])
def read_setting_by_name(
        db: Session = Depends(get_db),
    ):
    fetch = crud.read_setting_by_name(db, "public_key")
    return fetch.__dict__




# Role
@app.post("/role/", status_code=status.HTTP_201_CREATED, tags=["Role"])
def create_role(
        member: schemas.Role,
        db: Session = Depends(get_db),
        api_user: str | None = Header(default=None, convert_underscores=True),
        api_password: str | None = Header(default=None, convert_underscores=True),
    ):
    
    get_rbac(
        function_id=2,
        db=db,
        api_user=api_user,
        api_password=api_password,
        create=True
    )
    
    return crud.create_role(db, member)

@app.get("/role/", status_code=status.HTTP_200_OK, tags=["Role"])
def read_role(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db),
        api_user: str | None = Header(default=None, convert_underscores=True),
        api_password: str | None = Header(default=None, convert_underscores=True),
    ):
    
    get_rbac(
        function_id=2,
        db=db,
        api_user=api_user,
        api_password=api_password,
        read=True
    )
    
    return crud.read_role(db, skip, limit)

@app.get("/role/{id}", status_code=status.HTTP_200_OK, tags=["Role"], response_model=schemas.Role)
def read_role_by_id(
        id: int,
        db: Session = Depends(get_db),
        api_user: str | None = Header(default=None, convert_underscores=True),
        api_password: str | None = Header(default=None, convert_underscores=True),
    ):
    
    get_rbac(
        function_id=2,
        db=db,
        api_user=api_user,
        api_password=api_password,
        read=True
    )
    
    fetch = crud.read_role_by_id(db, id)
    fetch.__dict__
    return fetch.__dict__

@app.put("/role/", status_code=status.HTTP_201_CREATED, tags=["Role"], response_model=schemas.Role)
def update_role_by_id(
        role: schemas.Role,
        db: Session = Depends(get_db),
        api_user: str | None = Header(default=None, convert_underscores=True),
        api_password: str | None = Header(default=None, convert_underscores=True),
    ):
    
    get_rbac(
        function_id=2,
        db=db,
        api_user=api_user,
        api_password=api_password,
        update=True
    )
    
    update = crud.update_role_by_id(db, role)
    return update.__dict__

@app.delete("/role/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["Role"])
def delete_role_by_id(
        id: int,
        db: Session = Depends(get_db),
        api_user: str | None = Header(default=None, convert_underscores=True),
        api_password: str | None = Header(default=None, convert_underscores=True),
    ):
    
    get_rbac(
        function_id=2,
        db=db,
        api_user=api_user,
        api_password=api_password,
        delete=True
    )
    
    if crud.delete_role_by_id(db, id):
        return {'detail': 'deleted'}
    else:
        raise HTTPException(status_code=500, detail="failed deletion")



# assign
@app.post("/assign/", status_code=status.HTTP_201_CREATED, tags=["Assign"])
def create_assign(
        assign: schemas.Assign,
        db: Session = Depends(get_db),
       api_user: str | None = Header(default=None, convert_underscores=True),
        api_password: str | None = Header(default=None, convert_underscores=True),
    ):
    
    get_rbac(
        function_id=3,
        db=db,
        api_user=api_user,
        api_password=api_password,
        create=True
    )
    
    return crud.create_assign(db, assign)

@app.get("/assign/", status_code=status.HTTP_200_OK, tags=["Assign"])
def read_assign(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db),
        api_user: str | None = Header(default=None, convert_underscores=True),
        api_password: str | None = Header(default=None, convert_underscores=True),
    ):
    
    get_rbac(
        function_id=3,
        db=db,
        api_user=api_user,
        api_password=api_password,
        read=True
    )
    
    return crud.read_assign(db, skip, limit)

@app.get("/assign/{id}", status_code=status.HTTP_200_OK, tags=["Assign"], response_model=schemas.Assign)
def read_assign_by_id(
        id: int,
        db: Session = Depends(get_db),
        api_user: str | None = Header(default=None, convert_underscores=True),
        api_password: str | None = Header(default=None, convert_underscores=True),
    ):
    
    get_rbac(
        function_id=3,
        db=db,
        api_user=api_user,
        api_password=api_password,
        read=True
    )
    
    fetch = crud.read_assign_by_id(db, id)
    fetch.__dict__
    return fetch.__dict__

@app.put("/assign/", status_code=status.HTTP_201_CREATED, tags=["Assign"], response_model=schemas.Assign)
def update_assign_by_id(
        assign: schemas.Assign,
        db: Session = Depends(get_db),
        api_user: str | None = Header(default=None, convert_underscores=True),
        api_password: str | None = Header(default=None, convert_underscores=True),
    ):
    
    get_rbac(
        function_id=3,
        db=db,
        api_user=api_user,
        api_password=api_password,
        update=True
    )
    
    update = crud.update_assign_by_id(db, assign)
    return update.__dict__

@app.delete("/assign/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["Assign"])
def delete_member_by_id(
        id: int,
        db: Session = Depends(get_db),
        api_user: str | None = Header(default=None, convert_underscores=True),
        api_password: str | None = Header(default=None, convert_underscores=True),
    ):
    
    get_rbac(
        function_id=3,
        db=db,
        api_user=api_user,
        api_password=api_password,
        delete=True
    )
    
    if crud.delete_role_by_id(db, id):
        return {'detail': 'deleted'}
    else:
        raise HTTPException(status_code=500, detail="failed deletion")




# User
@app.post("/user/", status_code=status.HTTP_201_CREATED, tags=["User"])
def create_user(
        user: schemas.User,
        db: Session = Depends(get_db),
        api_user: str | None = Header(default=None, convert_underscores=True),
        api_password: str | None = Header(default=None, convert_underscores=True),
    ):
    
    get_rbac(
        function_id=4,
        db=db,
        api_user=api_user,
        api_password=api_password,
        create=True
    )
    
    return crud.create_user(db, user)

@app.get("/user/", status_code=status.HTTP_200_OK, tags=["User"])
def read_user(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db),
        api_user: str | None = Header(default=None, convert_underscores=True),
        api_password: str | None = Header(default=None, convert_underscores=True),
    ):
    
    get_rbac(
        function_id=4,
        db=db,
        api_user=api_user,
        api_password=api_password,
        read=True
    )
    
    fetch = crud.read_user(db, skip, limit)
    data = []
    for value in fetch:
        data.append({
            "id": value.id,
            "name": value.name,
            "hash": "***REDACTED***",
            "modified": value.modified,
            "created": value.created,
        })
        
    return data

@app.get("/user/{id}", status_code=status.HTTP_200_OK, tags=["User"], response_model=schemas.User)
def read_user_by_id(
        id: int,
        db: Session = Depends(get_db),
        api_user: str | None = Header(default=None, convert_underscores=True),
        api_password: str | None = Header(default=None, convert_underscores=True),
    ):
    
    get_rbac(
        function_id=4,
        db=db,
        api_user=api_user,
        api_password=api_password,
        read=True
    )
    
    fetch = crud.read_user_by_id(db, id)
    data = fetch.__dict__
    data['hash'] = "***REDACTED***"
    return data

@app.put("/user/", status_code=status.HTTP_201_CREATED, tags=["User"], response_model=schemas.User)
def update_user_by_id(
        user: schemas.User,
        db: Session = Depends(get_db),
        api_user: str | None = Header(default=None, convert_underscores=True),
        api_password: str | None = Header(default=None, convert_underscores=True),
    ):
    
    get_rbac(
        function_id=4,
        db=db,
        api_user=api_user,
        api_password=api_password,
        update=True
    )
    
    update = crud.update_user_by_id(db, user)
    return update.__dict__

@app.delete("/user/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["User"])
def delete_user_by_id(
        id: int,
        db: Session = Depends(get_db),
        api_user: str | None = Header(default=None, convert_underscores=True),
        api_password: str | None = Header(default=None, convert_underscores=True),
    ):
    
    get_rbac(
        function_id=4,
        db=db,
        api_user=api_user,
        api_password=api_password,
        delete=True
    )
    
    if crud.delete_user_by_id(db, id):
        return {'detail': 'deleted'}
    else:
        raise HTTPException(status_code=500, detail="failed deletion")




# Secret
@app.post("/secret/", status_code=status.HTTP_201_CREATED, tags=["Secret"])
def create_secret(
        secret: schemas.Secret,
        db: Session = Depends(get_db),
        api_user: str | None = Header(default=None, convert_underscores=True),
        api_password: str | None = Header(default=None, convert_underscores=True),
        server_side_encryption: bool | None = Header(default=False, convert_underscores=True),
    ):
    
    get_rbac(
        function_id=5,
        db=db,
        api_user=api_user,
        api_password=api_password,
        create=True
    )
    
    if server_side_encryption:
        pub_key = crud.read_setting_by_name(db, "public_key")
        data = schemas.Secret(
            name=secret.name,
            value=crypto.encrypt(
                bytes(pub_key.value, "UTF-8"),
                bytes(secret.value, "UTF-8")
            ),
            sse=server_side_encryption
        )
    else:
        data = schemas.Secret(
            name=secret.name,
            value=secret.value,
            sse=server_side_encryption
        )
    
    if crud.create_secret(db, data):
        return {"detail": "success"}
    else:
        raise HTTPException(status_code=500, detail="failed")

@app.get("/secret/", status_code=status.HTTP_200_OK, tags=["Secret"])
def read_secret(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db),
        api_user: str | None = Header(default=None, convert_underscores=True),
        api_password: str | None = Header(default=None, convert_underscores=True),
    ):
    
    get_rbac(
        function_id=5,
        db=db,
        api_user=api_user,
        api_password=api_password,
        read=True
    )
    
    fetch = crud.read_secret(db, skip, limit)
    data = []
    for values in fetch:
        data.append({
            "sse": values.sse,
            "id": values.id,
            "name": values.name,
            "value": "***REDACTED***",
            "modified": values.modified,
            "created": values.created
        })

    return data

# response_model=schemas.Secret
@app.get("/secret/{name}", status_code=status.HTTP_200_OK, tags=["Secret"], response_model=schemas.Secret)
def read_secret_by_name(
        name: str,
        db: Session = Depends(get_db),
        api_user: str | None = Header(default=None, convert_underscores=True),
        api_password: str | None = Header(default=None, convert_underscores=True),
    ):
    
    get_rbac(
        function_id=5,
        db=db,
        api_user=api_user,
        api_password=api_password,
        read=True
    )
    
    fetch = crud.read_secret_by_name(db, name)

    if fetch.sse:
        private_key = crud.read_setting_by_name(db, "private_key")
        encrypted_data = crud.read_secret_by_name(db, name)
        data = schemas.Secret(
            id=encrypted_data.id,
            name=encrypted_data.name,
            value=crypto.decrypt(
                bytes(private_key.value, "UTF-8"),
                encrypted_data.value
            ),
            modified=encrypted_data.modified
        )
        return data
    
    return fetch.__dict__


@app.put("/secret/", status_code=status.HTTP_201_CREATED, tags=["Secret"])
def update_secret_by_id(
        secret: schemas.Secret,
        db: Session = Depends(get_db),
        api_user: str | None = Header(default=None, convert_underscores=True),
        api_password: str | None = Header(default=None, convert_underscores=True),
        server_side_encryption: bool | None = Header(default=False, convert_underscores=True),
    ):
    
    get_rbac(
        function_id=5,
        db=db,
        api_user=api_user,
        api_password=api_password,
        update=True
    )
    
    if server_side_encryption:
        pub_key = crud.read_setting_by_name(db, "public_key")
        data = schemas.Secret(
            id=secret.id,
            name=secret.name,
            value=crypto.encrypt(
                bytes(pub_key.value, "UTF-8"),
                bytes(secret.value, "UTF-8")
            ),
            sse=server_side_encryption
        )
    else:
        data = schemas.Secret(
            id=secret.id,
            name=secret.name,
            value=secret.value,
            sse=server_side_encryption
        )

    if crud.update_secret_by_id(db, data):
        return {"detail": "success"}
    else:
        raise HTTPException(status_code=500, detail="failed")

@app.delete("/secret/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["Secret"])
def delete_secret_by_id(
        id: int,
        db: Session = Depends(get_db),
        api_user: str | None = Header(default=None, convert_underscores=True),
        api_password: str | None = Header(default=None, convert_underscores=True),
    ):
    
    get_rbac(
        function_id=5,
        db=db,
        api_user=api_user,
        api_password=api_password,
        delete=True
    )
    
    if crud.delete_secret_by_id(db, id):
        return {'detail': 'deleted'}
    else:
        raise HTTPException(status_code=500, detail="failed deletion")
