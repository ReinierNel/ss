from sqlalchemy.orm import Session
import crud, crypto
import logging

LOG_FORMAT = "{\"date\": \"%(asctime)s\", \"level\": \"%(levelname)s\", \"message\": \"%(message)s\", \"file\": \"%(filename)s\", \"line\": \"%(lineno)s\", \"function\": \"%(funcName)s\"}"
LOG_LEVEL = logging.DEBUG
logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)

def check_user(db: Session, name: str, password: str):
    check_user = crud.read_user_by_name(db, name)
    try:
        if crypto.check_password(password, check_user.hash):
            logging.debug(f'user {name} password match')
            return True
        else:
            logging.warn(f'user {name} password does not match')
    except:
        logging.error(f'unable to verify user {name} password')
    return False

def check_rbac(db: Session, user_name: str, fid: int, create: bool, read: bool, update: bool, delete: bool):
    user = crud.read_user_by_name(db, user_name)
    user_groups = crud.read_member_by_uid(db, user.id)

    required_rbac_state = {
        'fid': fid,
        'create': create,
        'read': read,
        'update': update,
        'delete': delete,
    }
    
    user_assigned_roles =  {
        'fid': None,
        'create': False,
        'read': False,
        'update': False,
        'delete': False,
    }

    roles = []

    # check if user has assignments 
    user_assignments = crud.read_assign_by_uid(db, user.id)
    for user_assign in user_assignments:
        get_user_roles = crud.read_role_by_id(db, user_assign.rid)
        for user_role in get_user_roles:
            roles.append({
                'fid': user_role.fid,
                'create': user_role.create,
                'read': user_role.read,
                'update': user_role.update,
                'delete': user_role.delete,
            })
            logging.debug(f'found role {user_role.name} for user {user.name}')

    # check if group user belongs to has assignments
    logging.debug(f'checking user {user.name} group membership')
    for group in user_groups:
        logging.debug(f'user {user.name} is a member of group id {group.id}')
        group_assignments = crud.read_assign_by_gid(db, group.id)
        for group_assign in group_assignments:            
            get_group_role = crud.read_role_by_id(db, group_assign.rid)
            logging.debug(f'role id {get_group_role.id} has function id {get_group_role.fid}')
            roles.append({
                'fid': get_group_role.fid,
                'create': get_group_role.create,
                'read': get_group_role.read,
                'update': get_group_role.update,
                'delete': get_group_role.delete,
            })
            logging.debug(f'found role {get_group_role.name} assigned to group id {group.id}')

    # check all users and group roles and update user_rbac_state
    logging.debug(f'parsing users {user.name} roles')
    for role in roles:
        if role['fid'] == fid:
            logging.debug(f'users {user.name} has a role that matches the function id {fid}')
            user_assigned_roles['fid'] = fid
            if role['create'] == create:
                logging.debug(f'users {user.name} matched create permission')
                user_assigned_roles['create'] = create
            if role['read'] == read:
                logging.debug(f'users {user.name} matched read permission')
                user_assigned_roles['read'] = read
            if role['update'] == update:
                logging.debug(f'users name {user.name} matched updated permission')
                user_assigned_roles['update'] = update
            if role['delete'] == delete:
                logging.debug(f'users {user.name} matched delete permission')
                user_assigned_roles['delete'] = delete
        else:
            logging.warn(f'users {user.name} has no role that matches the function id {fid}')

    # checked parsed roles against required rbac
    if user_assigned_roles == required_rbac_state:
        logging.debug(f'users {user.name} has the correct RBAC permission')
        return True
    else:
        logging.warn(f'users {user.name} does not have the correct RBAC permission')

    return False
