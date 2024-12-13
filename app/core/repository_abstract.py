from typing import List, Type, TypeVar, Generic, Optional

from app.config import session
from app.config import session

ModelType = TypeVar("ModelType")


class RepositoryAbstract(Generic[ModelType]):
    """Classe abstrata de repositório"""
    
    def __init__(self, model: Type[ModelType]):
        """
        Construtor para inicializar a entidade.
        :param model: Modelo do SQLAlchemy que será gerenciado pelo repositório.
        """
        self.model = model

    def find_all(self) -> List[ModelType]:
        """Retorna todos os registros"""
        return session.query(self.model).all()

    def find_first(self) -> Optional[ModelType]:
        """Retorna o primeiro registro"""
        return session.query(self.model).first()

    def find_by_id(self, entity_id: int) -> Optional[ModelType]:
        """Retorna um registro pelo ID"""
        return session.query(self.model).filter(self.model.id == entity_id).first()

    def save(self, entity: ModelType) -> ModelType:
        """
        Salva uma nova entidade no banco de dados.
        :param db: Sessão do banco de dados.
        :param entity: Entidade a ser salva.
        :return: Entidade salva.
        """
        session.add(entity)
        session.commit()
        session.refresh(entity)
        return entity

    def update(self, entity_id: int, entity_data: dict) -> Optional[ModelType]:
        """
        Atualiza um registro existente.
        :param db: Sessão do banco de dados.
        :param entity_id: ID da entidade a ser atualizada.
        :param entity_data: Dados para atualização.
        :return: Entidade atualizada ou None se não encontrada.
        """
        entity = self.find_by_id(entity_id)
        if not entity:
            return None
        for key, value in entity_data.items():
            setattr(entity, key, value)
        session.commit()
        session.refresh(entity)
        return entity

    def delete(self, entity_id: int) -> bool:
        """
        Exclui um registro pelo ID.
        :param db: Sessão do banco de dados.
        :param entity_id: ID da entidade a ser excluída.
        :return: True se excluído, False se não encontrado.
        """
        entity = self.find_by_id(entity_id)
        if not entity:
            return False
        session.delete(entity)
        session.commit()
        return True

    def find_last(self) -> Optional[ModelType]:
        """Retorna o último registro inserido"""
        return session.query(self.model).order_by(self.model.id.desc()).first()

    def save_or_update(self, entity: ModelType) -> ModelType:
        """
        Salva ou atualiza uma entidade.
        :param db: Sessão do banco de dados.
        :param entity: Entidade a ser salva ou atualizada.
        :return: Entidade salva ou atualizada.
        """
        session.merge(entity)
        session.commit()
        session.refresh(entity)
        return entity
