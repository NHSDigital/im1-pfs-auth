from pathlib import Path

import requests
import xmltodict

from ...domain.base_client import BaseClient
from ...domain.exception import (
    DownstreamError,
    ForbiddenError,
    InvalidValueError,
    NotFoundError,
)
from ...domain.forward_response_model import Demographics, ForwardResponse
from .models import (
    Application,
    Identifier,
    Patient,
    ServiceAccess,
    ServiceAccessDescription,
    ServiceAccessStatus,
    ServiceAccessStatusDescription,
    SessionRequestData,
    SessionRequestHeaders,
    SessionResponse,
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
        if self.request.use_mock:
            return self._mock_response()
        response = requests.post(
            url=self.request.forward_to,
            headers=self.get_headers(),
            data=self.get_data(),
            timeout=30,
        )
        response_json = xmltodict.parse(response.text)
        match response.status_code:
            case 201:
                return response_json
            case 400:
                raise InvalidValueError(response_json.get("Error", {}).get("message"))
            case 401:
                raise ForbiddenError(response_json.get("Error", {}).get("message"))
            case 404:
                raise NotFoundError(response_json.get("Error", {}).get("message"))
            case _:
                raise DownstreamError

    def transform_response(self, response: dict) -> ForwardResponse:
        """Function transform TPP client response.

        Args:
            response (dict): Response body from forwarded request

        Returns:
            ForwardResponse: Homogenised response with other clients
        """
        response = response.get("CreateSessionReply", {})
        proxy_link = response.get("User", {})
        proxy_person = proxy_link.get("Person", {})
        return SessionResponse(
            sessionId=response.get("@suid"),
            supplier=self.supplier,
            proxy=Demographics(
                firstName=proxy_person.get("PersonName", {}).get("@firstName"),
                surname=proxy_person.get("PersonName", {}).get("@surname"),
                title=proxy_person.get("PersonName", {}).get("@title"),
            ),
            patients=self._parse_patients(response),
        )

    def _mock_response(self) -> dict:
        """Function to return hard coded response.

        Returns:
            dict: Hard coded response rather than forwarding request to Emis client
        """
        with Path((BASE_DIR) / "data" / "mocked_response.xml", encoding="utf-8").open(
            "r"
        ) as f:
            mocked_response = f.read()
        return xmltodict.parse(mocked_response)

    def _parse_patients(self, data: dict) -> list[Patient]:
        """Parsing raw data from Client into structual model.

        Args:
            data (dict): Raw data containing information about multiple patients

        Returns:
            list[Patient]: Parsed information about multiple patients
        """
        # Extra Patient data
        patient_links = data.get("PatientAccess")
        if isinstance(
            patient_links, dict
        ):  # if only one patient xmltodict will not register this an array
            patient_links = [patient_links]

        parsed_patients = []
        for patient in patient_links:
            person = patient["Person"]
            raw_permissions = person.get("EffectiveServiceAccess", []).get(
                "ServiceAccess", []
            )
            parsed_patients.append(
                Patient(
                    firstName=person.get("PersonName", {}).get("@firstName"),
                    surname=person.get("PersonName", {}).get("@surname"),
                    title=person.get("PersonName", {}).get("@title"),
                    permissions=self._parse_permissions(raw_permissions),
                )
            )
        return parsed_patients

    def _parse_permissions(self, raw_permissions: dict) -> list[ServiceAccess]:
        return [
            ServiceAccess(
                description=ServiceAccessDescription(service["@description"]),
                serviceIdentifier=int(service["@serviceIdentifier"]),
                status=ServiceAccessStatus(service["@status"]),
                statusDescription=ServiceAccessStatusDescription(
                    service["@statusDesc"]
                ),
            )
            for service in raw_permissions
        ]
