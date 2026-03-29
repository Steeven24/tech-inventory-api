from passlib.context import CryptContext
from sqlalchemy.orm import Session

from models.user_model import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def _sanitize_user(self, user: User) -> dict:
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
        }

    def email_exists(self, email: str, exclude_user_id: int | None = None) -> bool:
        query = self.db.query(User).filter(User.email.ilike(email))

        if exclude_user_id is not None:
            query = query.filter(User.id != exclude_user_id)

        return self.db.query(query.exists()).scalar()

    def create_user(self, user_data):
        if self.email_exists(user_data.email):
            raise ValueError("Email already registered")

        hashed_password = self.hash_password(user_data.password)

        user = User(
            name=user_data.name,
            email=user_data.email,
            password=hashed_password,
            role=user_data.role,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return self._sanitize_user(user)

    def get_users(self):
        users = self.db.query(User).all()
        return [self._sanitize_user(user) for user in users]

    def get_user_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email.ilike(email)).first()

    def authenticate_user(self, email: str, password: str) -> User | None:
        user = self.get_user_by_email(email)
        if user is None:
            return None

        if not self.verify_password(password, user.password):
            return None

        return user

    def get_user_by_id(self, user_id: int):
        user = self.db.query(User).filter(User.id == user_id).first()
        if user is None:
            return None
        return self._sanitize_user(user)

    def update_user(self, user_id: int, user_data):
        user = self.db.query(User).filter(User.id == user_id).first()
        if user is None:
            return None

        if user_data.name is not None:
            user.name = user_data.name

        if user_data.email is not None:
            if self.email_exists(user_data.email, exclude_user_id=user_id):
                raise ValueError("Email already registered")
            user.email = user_data.email

        if user_data.password is not None:
            user.password = self.hash_password(user_data.password)

        if user_data.role is not None:
            user.role = user_data.role

        self.db.commit()
        self.db.refresh(user)
        return self._sanitize_user(user)

    def delete_user(self, user_id: int) -> bool:
        user = self.db.query(User).filter(User.id == user_id).first()
        if user is None:
            return False

        self.db.delete(user)
        self.db.commit()
        return True