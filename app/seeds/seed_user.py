"""This module refer user seed"""

from app.config import pwd_settings

def seeds(model) -> list:
    """This function refer generate user seeds"""
    users = [
        model(id=1, username="admin", password=pwd_settings.pwd_context.hash("1234"), email="HsRfE@example.com"),        
    ]

    for i in range(2, 15):
        users.append(model(id=i, username=f"user{i}", password=pwd_settings.pwd_context.hash("1234"), email=f"user{i}@example.com"))

    return users