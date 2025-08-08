import requests
from json import load
from requests import Response
from os import environ

from ..domain.base_client import BaseClient
from ..domain.forward_response_model import ForwardResponse, Demographics


class EmisClient(BaseClient):
    """An implementation of BaseClient tailored for forwarding requests to Emis's backend"""

    @property
    def supplier(self) -> str:
        return "EMIS"

    def get_data(self):
        return {
            "PatientIdentifier": {
                "IdentifierValue": self.request.patient_nhs_number,
                "IdentifierType": "NhsNumber",  # From enum ["Unknown", "NhsNumber", "ChiNumber"]
            },
            "CarerIdentifier": {
                "IdentifierValue": self.request.proxy_nhs_number,
                "IdentifierType": "NhsNumber",  # From enum ["Unknown", "NhsNumber", "ChiNumber"]
            },
            "PatientNationalPracticeCode": self.request.patient_ods_code,
        }

    def get_headers(self):
        return {
            "X-API-ApplicationId": self.request.application_id,  # The identity of the subsidiary
            "X-API-Version": "1",  # "The version of the API requested"
        }

    def forward_request(self) -> dict:
        if environ.get("USE_MOCK") == "True":
            with open(
                "app/api/infrastructure/data/mocked_emis_response.json",
                "r",
                encoding="utf-8",
            ) as f:
                data = load(f)
            return data
        else:
            response = requests.post(
                url=self.request.forward_to,
                headers=self.get_headers(),
                data=self.get_data(),
            )
            response.raise_for_status()
            return response.json()

    def transform_response(self, response: dict) -> ForwardResponse:
        user_patient_links = response.get("UserPatientLinks", [])
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
                if patient_link
            ],
        )
