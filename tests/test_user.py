from unittest.mock import patch
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
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


@patch("app.modules.user.repository.session")
@patch("app.modules.user.repository.UserRepository.find_by_username")
@patch("app.modules.user.repository.UserRepository.save")
def test_user_register_verify_if_not_exists(mock_save, mock_find, session):
    """
    Testa o registro de usuário verificando se o username não existe.
    """
    # Simula os retornos dos métodos do repositório
    mock_find.return_value = None  # Simula que o usuário não existe no banco
    mock_save.return_value = User(username="admin")  # Simula a criação do usuário

    # Instancia o serviço com o repositório mockado
    user_service = UserService(repository=UserRepository())

    # Chama o método de registro
    user_data = prepare_data_user()
    registered_user = user_service.register(user_data)

    # Asserções
    assert registered_user.username == "admin"
    assert isinstance(registered_user, User)

