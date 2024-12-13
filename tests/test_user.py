import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.modules.user.service import UserService
from app.modules.user.model import User
from app.modules.user.repository import UserRepository

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
    mock_find = mocker.patch("app.modules.user.repository.UserRepository.find_by_username")
    mock_save = mocker.patch("app.modules.user.repository.UserRepository.save")
    mock_session = mocker.patch("app.modules.user.repository.session")
    
    return mock_find, mock_save, mock_session

def test_register_user(mock_user_repository):
    """Test register user"""
    mock_find, mock_save, _ = mock_user_repository
    
    # Simule repository returns
    mock_find.return_value = None  # Simule user not exists
    mock_save.return_value = User(username="admin")  # Simule user saved

    # Instance service
    user_service = UserService(repository=UserRepository())

    user_data = prepare_data_user()  # Prepare user data
    registered_user = user_service.register(user_data)

    # Assertions
    assert registered_user.username == "admin"
    assert isinstance(registered_user, User)

