import os
from json import load
from pathlib import Path

import requests

from ...domain.base_client import BaseClient
from ...domain.forward_response_model import (
    Demographics,
    ForwardResponse,
    Patient,
    Permissions,
    ViewPermissions,
)
from .models import (
    Application,
    Identifier,
    SessionRequestData,
    SessionRequestHeaders,
)

BASE_DIR = Path(__file__).parent


class TPPClient(BaseClient):
    """An implementation of BaseClient tailored for forwarding requests to TPP's backend."""  # noqa: E501

    @property
    def supplier(self) -> str:
        """Property to hold information about the client supplier.

        Returns:
            str: Supplier name
        """
        return "TPP"

    def get_data(self) -> dict:
        """Function to create data to pass to TPP client.

        Returns:
            dict: Data dictionary
        """
        session_request = SessionRequestData(
            application=Application(provider_id=self.request.application_id),
            patient=Identifier(value=self.request.patient_nhs_number),
            patient_ods_code=self.request.patient_ods_code,
            proxy=Identifier(value=self.request.proxy_nhs_number),
        )
        return session_request.to_dict()

    def get_headers(self) -> dict:
        """Function to create headers to pass to TPP client.

        Returns:
            dict: Header dictionary
        """
        request_headers = SessionRequestHeaders()
        return request_headers.to_dict()

    def forward_request(self) -> dict:
        """Function to forward requests to TPP client.

        Returns:
            dict: Response body from forwarded request
        """
        if os.environ.get("USE_MOCK") == "True":
            return self._mock_response()
        response = requests.post(
            url=self.request.forward_to,
            headers=self.get_headers(),
            data=self.get_data(),
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def transform_response(self, response: dict) -> ForwardResponse:
        """Function transform TPP client response.

        Args:
            response (dict): Response body from forwarded request

        Returns:
            ForwardResponse: Homogenised response with other clients
        """
        proxy_link = response.get("User", {})
        proxy_person = proxy_link.get("Person", {})
        return ForwardResponse(
            sessionId=response.get("suid"),
            supplier=self.supplier,
            proxy=Demographics(
                firstName=proxy_person.get("PersonName", {}).get("firstName"),
                surname=proxy_person.get("PersonName", {}).get("surname"),
                title=proxy_person.get("PersonName", {}).get("title"),
            ),
            patients=self._parse_patients(response),
        )

    def _mock_response(self) -> dict:
        """Function to return hard coded response.

        Returns:
            dict: Hard coded response rather than forwarding request to Emis client
        """
        with Path((BASE_DIR) / "data" / "mocked_response.json").open("r") as f:
            return load(f)

    def _parse_patients(self, data: dict) -> list[Patient]:
        """Parsing raw data from Client into structual model.

        Args:
            data (dict): Raw data containing information about multiple patients

        Returns:
            list[Patient]: Parsed information about multiple patients
        """
        # Extra Patient data
        patient_links = data.get("PatientAccess", [{}])
        parsed_patinets = []
        for patient in patient_links:
            raw_permissions = patient.get("EffectiveServiceAccess", [])
            parsed_patinets.append(
                Patient(
                    firstName=patient.get("PersonName", {}).get("firstName"),
                    surname=patient.get("PersonName", {}).get("surname"),
                    title=patient.get("PersonName", {}).get("title"),
                    permissions=self._parse_permissions(raw_permissions),
                )
            )
        return parsed_patinets

    def _parse_permissions(self, raw_permissions: dict) -> Permissions:
        permissions_map = {
            # Key = desired field name
            # Value = (Desired Class for field, origin of value)
            "access_system_connect": (Permissions, "Access SystmConnect"),
            "book_appointments": (Permissions, "Appointments"),
            "change_pharamacy": (Permissions, "Access SystmConnect"),
            "messsage_practice": (Permissions, "Messaging"),
            "provide_information_to_practice": (
                Permissions,
                "Questionnaires",
            ),
            "request_medication": (Permissions, "Request Medication"),
            "update_demographics": (Permissions, None),  # EMIS only
            "manage_online_triage": (Permissions, "Access SystmConnect"),
            "medical_record": (ViewPermissions, "Detailed Coded Record"),
            "summary_medical_record": (ViewPermissions, "Summary Record"),
            "allergies_medical_record": (
                ViewPermissions,
                "Summary Record",
            ),
            "consultations_medical_record": (
                ViewPermissions,
                "Detailed Coded Record",
            ),
            "immunisations_medical_record": (
                ViewPermissions,
                "Detailed Coded Record",
            ),
            "documents_medical_record": (
                ViewPermissions,
                "Detailed Coded Record",
            ),
            "medication_medical_record": (
                ViewPermissions,
                "Summary Record",
            ),
            "problems_medical_record": (
                ViewPermissions,
                "Detailed Coded Record",
            ),
            "test_results_medical_record": (
                ViewPermissions,
                "Detailed Coded Record",
            ),
            "record_audit": (ViewPermissions, "Record Audit"),
            "record_sharing": (ViewPermissions, "Manage Sharing Rules And Requests"),
        }

        permission_kwargs = {}
        view_kwargs = {}

        for field_name, (target_model, origin) in permissions_map.items():
            # find the matching service by description
            service = next(
                (s for s in raw_permissions if s["description"] == origin), None
            )
            # bucket into correct model
            value = service["status"] == "A" if service else False
            if target_model is Permissions:
                permission_kwargs[field_name] = value
            elif target_model is ViewPermissions:
                view_kwargs[field_name] = value

        return Permissions(
            **permission_kwargs,
            view=ViewPermissions(**view_kwargs),
        )
