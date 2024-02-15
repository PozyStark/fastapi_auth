from abc import ABC, abstractmethod


class AbstractRepository(ABC):

    @abstractmethod
    async def add_one():
        raise NotImplementedError

    @abstractmethod
    async def add_many():
        raise NotImplementedError

    @abstractmethod
    async def find_one_or_none():
        raise NotImplementedError

    @abstractmethod
    async def find_all():
        raise NotImplementedError

    @abstractmethod
    async def update_one():
        raise NotImplementedError
    
    @abstractmethod
    async def update_many():
        raise NotImplementedError

    @abstractmethod
    async def update_all():
        raise NotImplementedError

    @abstractmethod
    async def delete():
        raise NotImplementedError