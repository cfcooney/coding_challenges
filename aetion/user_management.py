# User Management System
import datetime
from dataclasses import dataclass
from typing import Union

@dataclass
class User:
    name: str
    email: str
    age: int
    created: datetime.datetime = datetime.datetime.now()
    active: bool = True
    login_count: int = 0

    def __post_init__(self):
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("invalid name.")
        if not isinstance(self.email, str) or not self.email.strip:
            raise ValueError("invalid email.")
        if not isinstance(self.age, int):
            raise ValueError(f"age must be of type int, but is type {type(self.age)}.")
        if  self.age < 0:
            raise ValueError("invalid age.")
    
    def login(self):
        """Logs user into user management system."""
        if not self.active:
            raise ValueError(f"User {self.name} does not have an active account.")
        self.login_count += 1
    
    def deactivate(self):
        """Deactivate user account."""
        if not self.active:
            raise ValueError(f"No active user {self.name} to deactivate.")
        self.active = False
    
    def get_info(self) -> str:
        """Return User information details."""
        return f"{self.name}, {self.email} - Age: {self.age} - Logins: {self.login_count}"

class UserManager:
    def __init__(self):
        self.users: dict[str, User] = {}
    
    def add_user(self, name: str, email: str, age: int) -> User:
        """Add user to UserManager."""
        new_user = User(name, email, age)
        self.users[email] = new_user
        return new_user
    
    def find_user(self, email: str) -> Union[str, None]:
        """Find user by email."""
        if not isinstance(email, str) or not email.split():
            raise ValueError("invalid email address.")
        if not self.users.get(email):
            raise ValueError("User not in database.")
        return self.user.get(email)
    
    def get_active_users(self) -> list:
        """Find active users."""
        return [user for user in self.users.values() if user.active]
    
    def get_user_count(self) -> int:
        """Return user count."""
        return len(self.users)
    
    def delete_user(self, email: str):
        """Delete user from user manager based on email."""
        if not isinstance(email, str) or not email.split():
            raise ValueError("invalid email address.")
        del self.users[email]

if __name__ == "__main__":
    # Usage example
    manager = UserManager()
    manager.add_user("John Doe", "john@email.com", 25)
    manager.add_user("Jane Smith", "jane@email.com", 30)

    user1 = manager.find_user("john@email.com")
    if user1:
        user1.login()
        print(user1.get_info())