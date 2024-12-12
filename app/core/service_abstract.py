from typing import List, Type, TypeVar, Generic, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.repository_abstract import RepositoryAbstract
from app.commom.exceptions.information_not_found import InformationNotFound

# Tipo genérico para entidades do banco de dados
ModelType = TypeVar("ModelType")
# Tipo genérico para DTOs (Data Transfer Objects)
DTOType = TypeVar("DTOType", bound=BaseModel)

class ServiceAbstract(Generic[ModelType, DTOType]):
    """Classe abstrata de serviço para gerenciamento de dados."""

    def __init__(self, repository: RepositoryAbstract[ModelType]):
        """
        Construtor para inicializar o serviço com um repositório.
        :param repository: Instância do repositório associado ao modelo.
        """
        self.repository = repository

    def get_by_id(self, id: int) -> ModelType:
        """
        Busca um registro pelo ID.
        :param db: Sessão do banco de dados.
        :param id_model: ID do modelo a ser buscado.
        :return: Instância do modelo encontrado.
        :raises InformationNotFound: Caso o registro não seja encontrado.
        """
        instance = self.repository.find_by_id(id)
        if not instance:
            raise InformationNotFound(f"Registro com ID {id} não encontrado.")
        return instance

    def register(self, dto: DTOType) -> ModelType:
        """
        Registra um novo modelo no banco de dados.
        :param db: Sessão do banco de dados.
        :param dto: Dados para criação do modelo.
        :return: Instância do modelo criado.
        """
        entity = self.repository.model(**dto.model_dump())
        return self.repository.save(entity)

    def update(self, id: int, dto: DTOType) -> Optional[ModelType]:
        """
        Atualiza um modelo existente.
        :param db: Sessão do banco de dados.
        :param id_model: ID do modelo a ser atualizado.
        :param dto: Dados para atualização do modelo.
        :return: Instância do modelo atualizado ou None se não encontrado.
        """
        entity_data = dto.model_dump()
        return self.repository.update(id, entity_data)

    def remove(self, id: int) -> bool:
        """
        Remove um modelo existente pelo ID.
        :param db: Sessão do banco de dados.
        :param id_model: ID do modelo a ser removido.
        :return: True se o modelo foi removido, False caso contrário.
        """
        return self.repository.delete(id)

    def get_last(self) -> ModelType:
        """
        Obtém o último registro criado.
        :param db: Sessão do banco de dados.
        :return: Instância do último registro encontrado.
        :raises InformationNotFound: Caso não existam registros.
        """
        instance = self.repository.find_last()
        if not instance:
            raise InformationNotFound("Nenhum registro encontrado.")
        return instance

    def get_all(self) -> List[ModelType]:
        """
        Obtém todos os registros do banco de dados.
        :param db: Sessão do banco de dados.
        :return: Lista de instâncias do modelo.
        """
        return self.repository.find_all()

    def get_first(self) -> Optional[ModelType]:
        """
        Obtém o primeiro registro do banco de dados.
        :param db: Sessão do banco de dados.
        :return: Instância do primeiro registro ou None se não existir.
        """
        return self.repository.find_first()
