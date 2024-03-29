from datetime import datetime

from sqlalchemy import TIMESTAMP, Column, Integer, String

from db.base_class import Base


class User(Base):
    """
    Represents a user.

    Attributes:
        id (int): The unique identifier for the user.
        first_name (str): The user's first name.
        last_name (str): The user's last name.
        email (str): The user's email address.
        hashed_password (str): The user's hashed password.
        is_active (int): Whether the user is active or not.
        last_login (datetime): The date and time of the user's last login.
        created_at (datetime): The date and time the user was created.
        updated_at (datetime): The date and time the user was last updated.
    """

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False, index=True)
    last_name = Column(String(50), nullable=False, index=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Integer, nullable=False, default=1)
    last_login = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        TIMESTAMP, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
