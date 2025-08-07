from requests import Response

from .base_client import BaseClient
from domain.forward_response_model import ForwardResponse, Patient


class EmisClient(BaseClient):
    """An implementation of BaseClient tailored for forwarding requests to Emis's backend"""

    def get_headers(self):
        return {
            "X-API-ApplicationId": self.request.application_id,  # The identity of the subsidiary
            "X-API-Version": "1",  # "The version of the API requested"
        }

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

    def transform_response(self, response: Response) -> ForwardResponse:
        response_body = response.json()
        user_patient_links = response_body.get("UserPatientLinks", [])
        return ForwardResponse(
            session_id=response_body.get("SessionId"),
            first_name=response_body.get("FirstName"),
            surname=response_body.get("Surname"),
            title=response_body.get("Title"),
            patients=[
                Patient(
                    first_name=patient_link.get("Forenames"),
                    surname=patient_link.get("Surname"),
                    title=patient_link.get("Title"),
                )
                for patient_link in user_patient_links
                if patient_link
            ],
        )
