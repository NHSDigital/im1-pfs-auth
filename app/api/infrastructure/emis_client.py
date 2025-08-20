import os
from json import load
from pathlib import Path

import requests

from ..domain.base_client import BaseClient
from ..domain.forward_response_model import Demographics, ForwardResponse

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
        return {
            "PatientIdentifier": {
                "IdentifierValue": self.request.patient_nhs_number,
                "IdentifierType": "NhsNumber",
            },
            "CarerIdentifier": {
                "IdentifierValue": self.request.proxy_nhs_number,
                "IdentifierType": "NhsNumber",
            },
            "PatientNationalPracticeCode": self.request.patient_ods_code,
        }

    def get_headers(self) -> dict:
        """Function to create headers to pass to Emis client.

        Returns:
            dict: Header dictionary
        """
        return {
            "X-API-ApplicationId": self.request.application_id,
            "X-API-Version": "1",
        }

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
            ForwardResponse: Homogenesised response with other clients
        """
        user_patient_links = response.get("UserPatientLinks", [{}])
        return ForwardResponse(
            session_id=response.get("SessionId"),
            supplier=self.supplier,
            proxy=Demographics(
                first_name=response.get("FirstName"),
                surname=response.get("Surname"),
                title=response.get("Title"),
            ),
            patients=[
                Demographics(
                    first_name=patient_link.get("Forenames"),
                    surname=patient_link.get("Surname"),
                    title=patient_link.get("Title"),
                )
                for patient_link in user_patient_links
            ],
        )

    def __mock_response(self) -> dict:
        """Function to return hard coded response.

        Returns:
            dict: Hard coded response rather than forwarding request to Emis client
        """
        with Path((BASE_DIR) / "data" / "mocked_emis_response.json").open("r") as f:
            return load(f)
