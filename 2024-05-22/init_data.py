from datetime import datetime

from model import Role, User, engine
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

data_roles = dict(admin={"id": "admin"}, user={"id": "user"})

data_users = dict(
    admin={
        "id": "admin",
        "first_name": "Super",
        "last_name": "Admin",
        "email": "admin@yacr.com",
        "hashed_password": "$2b$12$yLRmKj2Gq3imyo9u674jBeEcvZW0WRbz9/zOyU323RJcGg/TKIyp2",
        "disabled": False,
        "creation_at": datetime.now(),
        "role_id": "admin",
        "bio": "YACR Admin",
        "age": 50,
    },
    alexcarrega={
        "id": "alexcarrega",
        "first_name": "Alex",
        "last_name": "Carrega",
        "email": "contact@alexcarrega.com",
        "hashed_password": "$2b$12$K38LDR2IovAIZhF2Cq9vAuCNeTFdJYie9EXp36h/62Fy9LBgMWa9C",
        "disabled": False,
        "creation_at": datetime.now(),
        "role_id": "user",
        "bio": "PhD, IT & Network Engineer",
        "age": 42,
    },
)


def insert_role(key):
    try:
        role = Role(**data_roles[key])
        print(role)
        with Session(engine) as session:
            try:
                session.add(role)
                session.commit()
                session.refresh(role)
                print(f"Role {role.id} created")
            except IntegrityError as ie:
                print(f"Error: {ie}")
    except Exception as e:
        print(f"Error: {e}")


def insert_user(key):
    try:
        user = User(**data_users[key])
        print(user)
        with Session(engine) as session:
            try:
                session.add(user)
                session.commit()
                session.refresh(user)
                print(f"User {user.id} created")
            except IntegrityError as ie:
                print(f"Error: {ie}")
    except Exception as e:
        print(f"Error: {e}")


insert_role("admin")
insert_role("user")
insert_user("admin")
insert_user("alexcarrega")
