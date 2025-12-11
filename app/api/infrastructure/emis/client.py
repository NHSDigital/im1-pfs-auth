from json import load
from pathlib import Path

import requests

from ...domain.base_client import BaseClient
from ...domain.exception import (
    DownstreamError,
    ForbiddenError,
    InvalidValueError,
    NotFoundError,
)
from ...domain.forward_response_model import Demographics, ForwardResponse
from .models import (
    Identifier,
    MedicalRecordPermissions,
    Patient,
    Permissions,
    SessionRequestData,
    SessionRequestHeaders,
)

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
        session_request = SessionRequestData(
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
        request_headers = SessionRequestHeaders(
            application_id=self.request.application_id
        )
        return request_headers.to_dict()

    def forward_request(self) -> dict:
        """Function to forward requests to Emis client.

        Returns:
            dict: Response body from forwarded request
        """
        if self.request.use_mock:
            return self._mock_response()
        response = requests.post(
            url=self.request.forward_to,
            headers=self.get_headers(),
            data=self.get_data(),
            timeout=30,
        )
        response_json = response.json()
        match response.status_code:
            case 201:
                return response_json
            case 400:
                raise InvalidValueError(response_json.get("message"))
            case 401:
                raise ForbiddenError(response_json.get("message"))
            case 404:
                raise NotFoundError(response_json.get("message"))
            case _:
                raise DownstreamError

    def transform_response(self, response: dict) -> ForwardResponse:
        """Function transform Emis client response.

        Args:
            response (dict): Response body from forwarded request

        Returns:
            ForwardResponse: Homogenised response with other clients
        """
        return ForwardResponse(
            sessionId=response.get("SessionId"),
            endUserSessionId=response.get("EndUserSessionId"),
            supplier=self.supplier,
            proxy=Demographics(
                firstName=response.get("FirstName"),
                surname=response.get("Surname"),
                title=response.get("Title"),
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
        patient_links = data.get("UserPatientLinks", [])
        parsed_patients = []
        for patient in patient_links:
            raw_permissions = patient.get("EffectiveServices", {})
            parsed_patients.append(
                Patient(
                    firstName=patient.get("FirstName"),
                    surname=patient.get("Surname"),
                    title=patient.get("Title"),
                    permissions=self._parse_permissions(raw_permissions),
                )
            )
        return parsed_patients

    def _parse_permissions(self, raw_permissions: dict) -> Permissions:
        return Permissions(
            appointmentsEnabled=raw_permissions.get("AppointmentsEnabled"),
            demographicsUpdateEnabled=raw_permissions.get("DemographicsUpdateEnabled"),
            epsEnabled=raw_permissions.get("EpsEnabled"),
            medicalRecordEnabled=raw_permissions.get("MedicalRecordEnabled"),
            onlineTriageEnabled=raw_permissions.get("OnlineTriageEnabled"),
            practicePatientCommunicationEnabled=raw_permissions.get(
                "PracticePatientCommunicationEnabled"
            ),
            prescribingEnabled=raw_permissions.get("PrescribingEnabled"),
            recordSharingEnabled=raw_permissions.get("RecordSharingEnabled"),
            recordViewAuditEnabled=raw_permissions.get("RecordViewAuditEnabled"),
            medicalRecord=MedicalRecordPermissions(
                recordAccessScheme=raw_permissions.get("MedicalRecord", {}).get(
                    "RecordAccessScheme"
                ),
                allergiesEnabled=raw_permissions.get("MedicalRecord", {}).get(
                    "AllergiesEnabled"
                ),
                consultationsEnabled=raw_permissions.get("MedicalRecord", {}).get(
                    "ConsultationsEnabled"
                ),
                immunisationsEnabled=raw_permissions.get("MedicalRecord", {}).get(
                    "ImmunisationsEnabled"
                ),
                documentsEnabled=raw_permissions.get("MedicalRecord", {}).get(
                    "DocumentsEnabled"
                ),
                medicationEnabled=raw_permissions.get("MedicalRecord", {}).get(
                    "MedicationEnabled"
                ),
                problemsEnabled=raw_permissions.get("MedicalRecord", {}).get(
                    "ProblemsEnabled"
                ),
                testResultsEnabled=raw_permissions.get("MedicalRecord", {}).get(
                    "TestResultsEnabled"
                ),
            ),
        )
