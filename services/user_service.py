from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self):
        self.users = []
        self.id_counter = 1
        
    def hashPassword(self, password: str) -> str:
        return pwd_context.hash(password)
    
    def createUser(self, user_data):
        hashedPassword = self.hashPassword(user_data.password)
        
        user = {
            "id": self.id_counter,
            "name": user_data.name,
            "email": user_data.email,
            "password": hashedPassword
        }
        self.users.append(user)
        self.id_counter+=1
        return {
            "id": user  ["id"],
            "name": user["name"],
            "email": user["email"]
        }
    
    def getUsers(self):
        return [{
            "id": user["id"],
            "name": user["name"],
            "email": user["email"]  
        }
        for user in self.users
        ]