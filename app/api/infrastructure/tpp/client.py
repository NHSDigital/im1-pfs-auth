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
            "accessSystemConnect": (Permissions, "Access SystmConnect"),
            "bookAppointments": (Permissions, "Appointments"),
            "changePharamacy": (Permissions, "Access SystmConnect"),
            "messagePractice": (Permissions, "Messaging"),
            "provideInformationToPractice": (
                Permissions,
                "Questionnaires",
            ),
            "requestMedication": (Permissions, "Request Medication"),
            "updateDemographics": (Permissions, None),  # EMIS only
            "manageOnlineTriage": (Permissions, "Access SystmConnect"),
            "medicalRecord": (ViewPermissions, "Detailed Coded Record"),
            "summaryMedicalRecord": (ViewPermissions, "Summary Record"),
            "allergiesMedicalRecord": (
                ViewPermissions,
                "Summary Record",
            ),
            "consultationsMedicalRecord": (
                ViewPermissions,
                "Detailed Coded Record",
            ),
            "immunisationsMedicalRecord": (
                ViewPermissions,
                "Detailed Coded Record",
            ),
            "documentsMedicalRecord": (
                ViewPermissions,
                "Detailed Coded Record",
            ),
            "medicationMedicalRecord": (
                ViewPermissions,
                "Summary Record",
            ),
            "problemsMedicalRecord": (
                ViewPermissions,
                "Detailed Coded Record",
            ),
            "testResultsMedicalRecord": (
                ViewPermissions,
                "Detailed Coded Record",
            ),
            "recordAudit": (ViewPermissions, "Record Audit"),
            "recordSharing": (ViewPermissions, "Manage Sharing Rules And Requests"),
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
