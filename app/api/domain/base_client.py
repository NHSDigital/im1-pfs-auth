from abc import ABC, abstractmethod

from .forward_request_model import ForwardRequest
from .forward_response_model import ForwardResponse


class BaseClient(ABC):
    """An abstract base class that defines a blueprint for all backend clients that forward requests to external systems and transforms the responses."""  # noqa: E501

    def __init__(self, request: ForwardRequest) -> None:
        """Initialises client with request argument."""
        self.request = request

    @property
    @abstractmethod
    def supplier(self) -> str:
        """Abstract property to hold information on who the supplier is."""

    @abstractmethod
    def get_data(self) -> dict:
        """Abstract method to retrieve data to forward onto the external system."""

    @abstractmethod
    def get_headers(self) -> dict:
        """Abstract method to retrieve headers to forward onto the external system."""

    @abstractmethod
    def forward_request(self) -> dict:
        """Abstract method to forward request onto the external system."""

    @abstractmethod
    def transform_response(self, response: dict) -> ForwardResponse:
        """Abstract method to transform the response into a homogenised response."""
