from sqlmodel import Session, select
from src.models.user_model import User
import logging

logger = logging.getLogger()


class UserDAO:
    
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, user_id: int) -> User | None:
        try:
            return self.session.get(User, user_id)
        except Exception as e:
            logger.error(f"Could not get user by email: {e}")
            return None

    def get_by_email(self, email: str) -> User | None:
        try:
            statement = select(User).where(User.email == email)
            return self.session.exec(statement).first()
        except Exception as e:
            logger.error(f"Could not get user by email: {e}")
            return None

    def create(self, user: User) -> User | None:
        try:
            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)
            return user
        except Exception as e:
            self.session.rollback()
            logger.error(f"Could not create user: {e}")
            return None