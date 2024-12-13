from typing import List, Type, TypeVar, Generic, Optional

from app.config import session
from app.config import session

ModelType = TypeVar("ModelType")


class RepositoryAbstract(Generic[ModelType]):
    """Abstract class for repository"""
    
    def __init__(self, model: Type[ModelType]):
        """
        Constructor for repository.
        :param model: Model class.
        """
        self.model = model

    def find_all(self) -> List[ModelType]:
        """Returns all records"""
        return session.query(self.model).all()

    def find_first(self) -> Optional[ModelType]:
        """Returns the first record"""
        return session.query(self.model).first()

    def find_by_id(self, entity_id: int) -> Optional[ModelType]:
        """Return record by id"""
        return session.query(self.model).filter(self.model.id == entity_id).first()

    def save(self, entity: ModelType) -> ModelType:
        """Save record"""
        session.add(entity)
        session.commit()
        session.refresh(entity)
        return entity

    def update(self, entity_id: int, entity_data: dict) -> Optional[ModelType]:
        """Update record"""
        entity = self.find_by_id(entity_id)
        if not entity:
            return None
        for key, value in entity_data.items():
            setattr(entity, key, value)
        session.commit()
        session.refresh(entity)
        return entity

    def delete(self, entity_id: int) -> bool:
        """Delete record"""
        entity = self.find_by_id(entity_id)
        if not entity:
            return False
        session.delete(entity)
        session.commit()
        return True

    def find_last(self) -> Optional[ModelType]:
        """Returns the last record"""
        return session.query(self.model).order_by(self.model.id.desc()).first()

    def save_or_update(self, entity: ModelType) -> ModelType:
        """Save or update record"""
        session.merge(entity)
        session.commit()
        session.refresh(entity)
        return entity
