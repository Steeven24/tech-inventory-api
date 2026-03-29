from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self):
        self.users = []
        self.id_counter = 1

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def _sanitize_user(self, user: dict) -> dict:
        return {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
        }

    def _find_user_index_by_id(self, user_id: int) -> int:
        for index, user in enumerate(self.users):
            if user["id"] == user_id:
                return index
        return -1

    def email_exists(self, email: str, exclude_user_id: int | None = None) -> bool:
        email_value = email.lower()
        for user in self.users:
            if user["email"].lower() == email_value and user["id"] != exclude_user_id:
                return True
        return False

    def create_user(self, user_data):
        if self.email_exists(user_data.email):
            raise ValueError("Email already registered")

        hashed_password = self.hash_password(user_data.password)

        user = {
            "id": self.id_counter,
            "name": user_data.name,
            "email": user_data.email,
            "password": hashed_password,
        }
        self.users.append(user)
        self.id_counter += 1
        return self._sanitize_user(user)

    def get_users(self):
        return [self._sanitize_user(user) for user in self.users]

    def get_user_by_id(self, user_id: int):
        user_index = self._find_user_index_by_id(user_id)
        if user_index == -1:
            return None
        return self._sanitize_user(self.users[user_index])

    def update_user(self, user_id: int, user_data):
        user_index = self._find_user_index_by_id(user_id)
        if user_index == -1:
            return None

        user = self.users[user_index]

        if user_data.name is not None:
            user["name"] = user_data.name

        if user_data.email is not None:
            if self.email_exists(user_data.email, exclude_user_id=user_id):
                raise ValueError("Email already registered")
            user["email"] = user_data.email

        if user_data.password is not None:
            user["password"] = self.hash_password(user_data.password)

        self.users[user_index] = user
        return self._sanitize_user(user)

    def delete_user(self, user_id: int) -> bool:
        user_index = self._find_user_index_by_id(user_id)
        if user_index == -1:
            return False

        self.users.pop(user_index)
        return True