from sqlalchemy import Column, Table, text
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship
from sqlalchemy.schema import Index, UniqueConstraint
from sqlalchemy.types import BIGINT, INT, TIMESTAMP, Boolean, Date, Integer, String

from src.libstreak.database.connect import create_alchemy_engine


class Base(DeclarativeBase):
    pass


engine = create_alchemy_engine()
DEFAULT_UPDATE = text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")


class Streak(Base):
    __tablename__ = "streak"

    id_streak = Column(INT, primary_key=True)
    title = Column(String(100), nullable=False, unique=True)
    start_date = Column(TIMESTAMP, nullable=False, index=True)
    end_date = Column(TIMESTAMP, nullable=True, index=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False, index=True)
    updated_at = Column(TIMESTAMP, server_default=DEFAULT_UPDATE, nullable=False)


class StreakMember(Base):
    __tablename__ = "streak_member"

    id_streak_member = Column(INT, primary_key=True)
    id_streak = Column(INT, nullable=False)
    id_user = Column(INT, nullable=False, unique=True)
    joined_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False, index=True)

    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False)


class User(Base):
    __tablename__ = "user"

    id_user = Column(INT, primary_key=True)
    username = Column(String(50), nullable=False, unique=True, index=True)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    university = Column(String(100), nullable=True)
    degree_title = Column(String(100), nullable=True)
    graduation_year = Column(INT, nullable=True)
    company = Column(String(50), nullable=True)
    email = Column(String(50), nullable=True)
    phone = Column(String(50), nullable=True)
    home_country = Column(String(50), nullable=True)
    city = Column(String(50), nullable=True)

    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=DEFAULT_UPDATE, nullable=False)


class UserProfile(Base):
    __tablename__ = "user_profile"

    id_user_profile = Column(INT, primary_key=True)
    id_user = Column(INT, nullable=False)
    id_profile = Column(INT, nullable=False)  # linked_in, codeforces, leetcode, github
    url = Column(String(200), nullable=False)

    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=DEFAULT_UPDATE, nullable=False)


class Profile(Base):
    __tablename__ = "profile"

    id_profile = Column(INT, primary_key=True)
    code = Column(String(50), nullable=False, unique=True)  # linked_in, codeforces, leetcode, github
    name = Column(String(50), nullable=False, unique=True)  # linked_in, codeforces, leetcode, github
    url = Column(String(50), nullable=False)


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


if __name__ == "__main__":
    pass
