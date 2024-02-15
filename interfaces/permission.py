from abc import ABC, abstractmethod


class AbstractPermission(ABC):

    auto_error: bool = True

    @abstractmethod
    def has_permission():
        pass