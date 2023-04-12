from sqlalchemy.orm import Session
import crud, crypto

def check_user(db: Session, name: str, password: str):
    check_user = crud.read_user_by_name(db, name)
    try:
        if crypto.check_password(password, check_user.hash):
            return True
    except:
        pass
    return False

def check_rbac(db: Session, name: str, fid: int, read: bool, write: bool):
    user = crud.read_user_by_name(db, name)
    user_groups = crud.read_member_by_uid(db, user.id)
    try:
        for group in user_groups:
            group_roles = crud.read_assign_by_gid(db, group.id)
            for role_id in group_roles:
                role = crud.read_role_by_id(db, role_id.rid)
                if role.fid == fid:
                    if role.read == read or role.write == write:
                        return True
    except:
        pass
    
    return False