import pytest
from user_management import User, UserManager


def test_create_user():
    user = User("Ciaran Cooney", "ciaranfcooney@gmail.com", 38)
    assert user.active

def test_n_active_users():
    manager = UserManager()
    manager.add_user("John Doe", "john@email.com", 25)
    manager.add_user("Jane Smith", "jane@email.com", 30)
    manager.add_user("Ciaran Cooney", "ciaranfcooney@gmail.com", 38)
    manager.delete_user("ciaranfcooney@gmail.com")
    assert len(manager.get_active_users()) == 2