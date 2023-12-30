from abc import ABC, abstractmethod

from fastapi import HTTPException
from interfaces import AbstractPermission
from exceptions import UNAUTHORIZED_NOT_PERMITED
from core.request import AuthRequest
    


