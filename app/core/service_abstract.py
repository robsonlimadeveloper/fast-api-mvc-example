from typing import List, TypeVar, Generic, Optional
from pydantic import BaseModel
from app.core.repository_abstract import RepositoryAbstract
from app.commom.exceptions.information_not_found import InformationNotFound

ModelType = TypeVar("ModelType")
DTOType = TypeVar("DTOType", bound=BaseModel)

class ServiceAbstract(Generic[ModelType, DTOType]):
    """Abstract class for service"""

    def __init__(self, repository: RepositoryAbstract[ModelType]):
        """
        Constructor for service.
        :param repository: Repository class.
        """
        self.repository = repository

    def get_by_id(self, id: int) -> ModelType:
        """Get model by id"""
        instance = self.repository.find_by_id(id)
        if not instance:
            raise InformationNotFound(f"Register {id} not found.")
        return instance

    def register(self, dto: DTOType) -> ModelType:
        """Register model"""
        entity = self.repository.model(**dto.model_dump())
        return self.repository.save(entity)

    def update(self, id: int, dto: DTOType) -> Optional[ModelType]:
        """Update model"""
        entity_data = dto.model_dump()
        return self.repository.update(id, entity_data)

    def remove(self, id: int) -> bool:
        """Remove model"""
        return self.repository.delete(id)

    def get_last(self) -> ModelType:
        """Get last model"""
        instance = self.repository.find_last()
        if not instance:
            raise InformationNotFound("Information not found.")
        return instance

    def get_all(self) -> List[ModelType]:
        """Get all models"""
        return self.repository.find_all()

    def get_first(self) -> Optional[ModelType]:
        """
        get first
        """
        return self.repository.find_first()
