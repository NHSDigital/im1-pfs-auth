from abc import ABC, abstractmethod

from .forward_request_model import ForwardRequest
from .forward_response_model import ForwardResponse


class BaseClient(ABC):
    """An abstract base class that defines a blueprint for all backend clients that forward requests to external systems and transforms the responses"""

    def __init__(self, request: ForwardRequest):
        self.request = request

    @property
    @abstractmethod
    def supplier(self) -> str:
        pass

    @abstractmethod
    def get_data(self) -> dict:
        pass

    @abstractmethod
    def get_headers(self) -> dict:
        pass

    @abstractmethod
    def forward_request(self) -> dict:
        pass

    @abstractmethod
    def transform_response(self, response: dict) -> ForwardResponse:
        pass
