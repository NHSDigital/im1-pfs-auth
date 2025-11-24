import os
from json import load
from pathlib import Path

import requests

from ...domain.base_client import BaseClient
from ...domain.forward_response_model import Demographics, ForwardResponse
from .models import CreateSessionRequestData, CreateSessionRequestHeaders, Identifier

BASE_DIR = Path(__file__).parent


class EmisClient(BaseClient):
    """An implementation of BaseClient tailored for forwarding requests to Emis's backend."""  # noqa: E501

    @property
    def supplier(self) -> str:
        """Property to hold information about the client supplier.

        Returns:
            str: Supplier name
        """
        return "EMIS"

    def get_data(self) -> dict:
        """Function to create data to pass to Emis client.

        Returns:
            dict: Data dictionary
        """
        session_request = CreateSessionRequestData(
            patient=Identifier(value=self.request.patient_nhs_number),
            patient_ods_code=self.request.patient_ods_code,
            proxy=Identifier(value=self.request.proxy_nhs_number),
        )
        return session_request.to_dict()

    def get_headers(self) -> dict:
        """Function to create headers to pass to Emis client.

        Returns:
            dict: Header dictionary
        """
        request_headers = CreateSessionRequestHeaders(
            application_id=self.request.application_id
        )
        return request_headers.to_dict()

    def forward_request(self) -> dict:
        """Function to forward requests to Emis client.

        Returns:
            dict: Response body from forwarded request
        """
        if os.environ.get("USE_MOCK") == "True":
            return self.__mock_response()
        response = requests.post(
            url=self.request.forward_to,
            headers=self.get_headers(),
            data=self.get_data(),
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def transform_response(self, response: dict) -> ForwardResponse:
        """Function transform Emis client response.

        Args:
            response (dict): Response body from forwarded request

        Returns:
            ForwardResponse: Homogenised response with other clients
        """
        patient_links = response.get("UserPatientLinks", [{}])
        return ForwardResponse(
            sessionId=response.get("SessionId"),
            endUserSessionId=response.get("EndUserSessionId"),
            supplier=self.supplier,
            proxy=Demographics(
                firstName=response.get("FirstName"),
                surname=response.get("Surname"),
                title=response.get("Title"),
            ),
            patients=[
                Demographics(
                    firstName=patient_link.get("FirstName"),
                    surname=patient_link.get("Surname"),
                    title=patient_link.get("Title"),
                )
                for patient_link in patient_links
            ],
        )

    def __mock_response(self) -> dict:
        """Function to return hard coded response.

        Returns:
            dict: Hard coded response rather than forwarding request to Emis client
        """
        with Path((BASE_DIR) / "data" / "mocked_response.json").open("r") as f:
            return load(f)
