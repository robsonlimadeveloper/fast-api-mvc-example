import pytest
from gettext import find
from fastapi.testclient import TestClient
from app.main import app
from app.modules.user.service import UserService
from app.modules.user.model import User
from app.modules.user.exceptions import NameDuplicateException,\
                                        UserNotFoundException,\
                                        UserNotDeleteYourselfException

client = TestClient(app)

def prepare_data_user() -> dict:
    """ User data to register """
    return {
        "username": "admin",
        "password": "1234"
    }

@pytest.fixture
def mock_user_repository(mocker):
    """
    Mock user repository
    """
    mock_repo = mocker.Mock()
    mock_repo.find_by_username = mocker.Mock()
    mock_repo.save = mocker.Mock()
    
    return mock_repo

@pytest.fixture
def mock_auth_service(mocker):
    """
    Mock auth service
    """
    mock_service = mocker.Mock()
    mock_service.get_current_user = mocker.Mock()
    return mock_service


def test_register_user(mock_user_repository):
    """Test register user"""
    mock_user_repository.find_by_username.return_value = None
    mock_user_repository.save.return_value = User(username="admin")

    user_service = UserService(repository=mock_user_repository)

    user_data: dict = prepare_data_user()
    registered_user = user_service.register(user_data)

    assert registered_user.username == user_data["username"]
    assert isinstance(registered_user, User)

    mock_user_repository.find_by_username.assert_called_once_with(user_data["username"])
    mock_user_repository.save.assert_called_once()


def test_register_user_duplicate(mock_user_repository):
    """Test register user duplicate"""
    mock_user_repository.find_by_username.return_value = User(username="admin")

    user_service = UserService(repository=mock_user_repository)

    user_data: dict = prepare_data_user()
    with pytest.raises(NameDuplicateException) as exc_info:
        user_service.register(user_data)

    assert isinstance(exc_info.value, NameDuplicateException)

def test_update_user(mock_user_repository):
    """Test update user"""
    mock_user_repository.find_by_id.return_value = User(username="admin")
    mock_user_repository.update.return_value = User(username="admin")

    user_service = UserService(repository=mock_user_repository)

    user_data: dict = prepare_data_user()

    updated_user = user_service.update(1, user_data)

    assert updated_user.username == user_data["username"]
    assert isinstance(updated_user, User)

def test_update_user_not_exists(mock_user_repository):
    """Test update user not exists"""
    mock_user_repository.find_by_id.return_value = None

    
    user_service = UserService(repository=mock_user_repository)

    user_data: dict = prepare_data_user()

    with pytest.raises(UserNotFoundException) as exc_info:
        user_service.update(1, user_data)

    assert isinstance(exc_info.value, UserNotFoundException)

def test_get_user_by_username(mock_user_repository):
    """Test get user by username"""
    mock_user_repository.find_by_username.return_value = User(username="admin")

    user_service = UserService(repository=mock_user_repository)

    user = user_service.get_user_by_username("admin")

    assert user.__dict__["username"] == "admin"
    assert isinstance(user, User)

def test_get_user_by_id(mock_user_repository):
    """Test get user by id"""
    mock_user_repository.find_by_id.return_value = User(id=1, username="admin")

    user_service = UserService(repository=mock_user_repository)

    user = user_service.get_by_id(1)

    assert user.__dict__["id"] == 1
    assert user.__dict__["username"] == "admin"
    assert isinstance(user, User)
