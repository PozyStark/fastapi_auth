from datetime import datetime
from sqlalchemy.orm import declarative_base
from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, MetaData, String
from config import APP_PREFIX
from schemas.role import RoleSchema


metadata = MetaData()
Base = declarative_base(metadata=metadata)


class Role(Base):

    __tablename__ = f'{APP_PREFIX}_role'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    
    def to_read_model(self) -> RoleSchema:
        return RoleSchema(
            id=self.id,
            name=self.name
        )

class Group(Base):
    __tablename__ = f'{APP_PREFIX}_group'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)


class Permission(Base):

    __tablename__ = f'{APP_PREFIX}_permission'

    id = Column(Integer, primary_key=True, autoincrement=True)
    codename = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)


class User(Base):
    __tablename__ = f'{APP_PREFIX}_user'

    id = Column(String, primary_key=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, nullable=True, index=True)
    first_name = Column(String, nullable=True)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    last_updated = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    last_login = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_stuff = Column(Boolean, default=False, nullable=False)
    age = Column(Integer, nullable=True)
    avatar = Column(String, nullable=True)


class UserGroup(Base):
    __tablename__ = f'{APP_PREFIX}_user_group'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey(User.id), nullable=False, index=True)
    group_id = Column(Integer, ForeignKey(Group.id), nullable=False)


class UserRole(Base):
    __tablename__ = f'{APP_PREFIX}_user_role'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey(User.id), nullable=False, index=True)
    role_id = Column(Integer, ForeignKey(Role.id), nullable=False)


class UserPermission(Base):
    __tablename__ = f'{APP_PREFIX}_user_perrmission'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey(User.id), nullable=False)
    permission_id = Column(Integer, ForeignKey(Permission.id), nullable=False)


class RolePermission(Base):
    __tablename__ = f'{APP_PREFIX}_role_permission'

    id = Column(Integer, primary_key=True, autoincrement=True)
    role_id = Column(Integer, ForeignKey(Role.id), nullable=False)
    permission_id = Column(Integer, ForeignKey(Permission.id), nullable=False)


class GroupPermission(Base):
    __tablename__ = f'{APP_PREFIX}_group_permission'

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer, ForeignKey(Group.id), nullable=False)
    permission_id = Column(Integer, ForeignKey(Permission.id), nullable=False)


class TokenSession(Base):
    __tablename__ = f'{APP_PREFIX}_token_session'

    id = Column(String, primary_key=True, index=True)
    temp_id = Column(String, nullable=False)
    user_id = Column(String, ForeignKey(User.id), nullable=False, index=True)
    expire = Column(TIMESTAMP, nullable=False)
    is_active = Column(Boolean, nullable=False)

