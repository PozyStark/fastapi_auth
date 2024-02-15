from abc import ABC, abstractmethod


class AbstractPermission(ABC):

    @abstractmethod
    def has_permission():
        pass