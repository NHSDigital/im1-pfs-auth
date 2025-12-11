from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from app.api.domain.forward_response_model import Demographics, ForwardResponse


class Application(BaseModel):
    """Base Model for Application."""

    provider_id: str
    name: str = "NhsApp"  # Hardcoded placeholders
    version: str = "1.0"
    device_type: str = "NhsApp"


class Identifier(BaseModel):
    """Base Model for identifiers."""

    value: str
    type: str = "NhsNumber"


class SessionRequestData(BaseModel):
    """Base Model for the request data required to create a session."""

    application: Application
    patient: Identifier
    patient_ods_code: str
    proxy: Identifier
    api_version: str = "1"

    def to_dict(self) -> dict:
        """Converts Class into dictionary."""
        return {
            "apiVersion": self.api_version,
            "uuid": str(uuid4()),
            "User": {
                "Identifier": {"value": self.proxy.value, "type": self.proxy.type}
            },
            "Patient": {
                "Identifier": {"value": self.patient.value, "type": self.patient.type},
                "UnitId": self.patient_ods_code,
            },
            "Application": {
                "name": self.application.name,
                "version": self.application.version,
                "providerId": self.application.provider_id,
                "deviceType": self.application.device_type,
            },
        }


class SessionRequestHeaders(BaseModel):
    """Base Model for the request headers required to create a session."""

    type: str = "CreateSession"

    def to_dict(self) -> dict:
        """Converts Class into dictionary."""
        return {
            "type": self.type,
        }


class ServiceAccessDescription(Enum):
    """Enum Class for Service Access Description."""

    FULL_CLINCAL_RECORD = "Full Clinical Record"
    APPOINTMENTS = "Appointments"
    REQUEST_MEDICATION = "Request Medication"
    QUESTIONNAIRES = "Questionnaires"
    SUMMARY_RECORD = "Summary Record"
    DETAILED_CODED_RECORD = "Detailed Coded Record"
    MESSAGING = "Messaging"
    VIEW_SHARING_STATUS = "View Sharing Status"
    RECORD_AUDIT = "Record Audit"
    CHANGE_PARMACY = "Change Pharmacy"
    MANAGE_SCHARING_RULES_AND_REQUESTS = "Manage Sharing Rules And Requests"
    ACCESS_SYSTM_CONNECT = "Access SystmConnect"


class ServiceAccessStatus(Enum):
    """Enum Class for Service Access Status."""

    AVAILABLE = "A"
    UNAVAILABLE = "U"
    NOT_OFFERED = "N"
    GMS_REGISTERED_PATEINTS_ONLY = "G"
    OTHER = "O"


class ServiceAccessStatusDescription(Enum):
    """Enum Class for Service Access Status Description."""

    AVAILABLE = "Available"
    UNAVAILABLE = "Unavailable"
    NOT_OFFERED = "Not offered by unit"
    GMS_REGISTERED_PATEINTS_ONLY = "Only available to GMS registered patients"
    OTHER = "Other"


class ServiceAccess(BaseModel):
    """Base Model for Service Access which holds data per permission."""

    model_config = ConfigDict(alias_generator=to_camel)

    description: ServiceAccessDescription
    service_identifier: int
    status: ServiceAccessStatus
    status_description: ServiceAccessStatusDescription


class Patient(Demographics):
    """Base Model for Patient."""

    permissions: list[ServiceAccess]


class SessionResponse(ForwardResponse):
    """Extension of Forward Response."""

    model_config = ConfigDict(alias_generator=to_camel)

    patients: list[Patient]
