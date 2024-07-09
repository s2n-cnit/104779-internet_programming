#!/usr/bin/env -S poetry run python

# import os

# db_filepath = "yalb.db"
# if os.path.exists(db_filepath):
#     os.remove(db_filepath)
import os
from datetime import datetime  # noqa: E402

from config import db_path

if os.path.exists(db_path):
    os.remove(db_path)

from model import Role, User, engine  # noqa: E402
from passlib.context import CryptContext  # noqa: E402
from sqlalchemy.exc import IntegrityError  # noqa: E402
from sqlmodel import Session  # noqa: E402

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

data_roles = dict(
    admin={"id": "admin", "password": "admin"},
    user={"id": "user", "password": "test-me"},
)

data_users = dict(
    admin={
        "id": "admin",
        "first_name": "Super",
        "last_name": "Admin",
        "email": "admin@yacr.com",
        "password": pwd_context.hash(data_roles["admin"]["password"]),
        "disabled": False,
        "created_at": datetime.now(),
        "created_by_id": "admin",
        "role_id": "admin",
        "bio": "Admin",
        "age": 50,
    },
    alexcarrega={
        "id": "alexcarrega",
        "first_name": "Alex",
        "last_name": "Carrega",
        "email": "contact@alexcarrega.com",
        "password": pwd_context.hash(data_roles["user"]["password"]),
        "disabled": False,
        "created_at": datetime.now(),
        "created_by_id": "admin",
        "role_id": "user",
        "bio": "PhD, IT & Network Engineer",
        "age": 42,
    },
)


def insert_role(key):
    try:
        role = Role(**data_roles[key])
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
