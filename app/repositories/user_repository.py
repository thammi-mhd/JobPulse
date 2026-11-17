from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> User | None:
        return self.db.execute(select(User).where(User.email == email)).scalar_one_or_none()

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()

    def create_user(self, username: str, email: str, hashed_password: str) -> User:
        new_user = User(username=username, email=email, hashed_password=hashed_password)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def update_username(self, user: User, new_username: str) -> User:

        user.username = new_username
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_email(self, user: User, new_email: str) -> User:
        user.email = new_email
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_password(self, user: User, old_password: str,  new_hashed_password: str) -> User:
        if user.hashed_password != old_password:
            raise ValueError("Old password does not match")
        user.hashed_password = new_hashed_password
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user: User) -> None:
        self.db.delete(user)
        self.db.commit()

    def users(self):
        statement = select(User)
        result = self.db.execute(statement).scalars().all()
        return result