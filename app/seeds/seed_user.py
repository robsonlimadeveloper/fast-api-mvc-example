"""This module refer user seed"""

from app.config import pwd_settings

def seeds(model) -> list:
    """This function refer generate user seeds"""
    users = [
        model(id=1, username="admin", password=pwd_settings.pwd_context.hash("1234")),
        model(id=2, username="user1", password=pwd_settings.pwd_context.hash("1234")),
    ]
    return users