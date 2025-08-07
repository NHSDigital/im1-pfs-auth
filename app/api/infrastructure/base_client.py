import requests
from abc import ABC, abstractmethod
from requests import Response

from domain.forward_request_model import ForwardRequest
from domain.forward_response_model import ForwardResponse


class BaseClient(ABC):
    """An abstract base class that defines a blueprint for all backend clients that forward requests to external systems and transforms the responses"""

    def __init__(self, request: ForwardRequest):
        self.request = request

    @abstractmethod
    def get_data(self) -> dict:
        pass

    @abstractmethod
    def get_headers(self) -> dict:
        pass

    @abstractmethod
    def transform_response(self, response: Response) -> ForwardResponse:
        pass

    def forward_request(self) -> Response:
        response = requests.post(
            url=self.request.forward_to,
            headers=self.get_headers(),
            data=self.get_data(),
        )
        response.raise_for_status()
        return response
