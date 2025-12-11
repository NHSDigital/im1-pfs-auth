from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from app.api.domain.forward_response_model import Demographics, ForwardResponse


class Identifier(BaseModel):
    """Base Model for identifiers."""

    value: str
    type: str = "NhsNumber"


class SessionRequestData(BaseModel):
    """Base Model for the request data required to create a session."""

    patient: Identifier
    patient_ods_code: str
    proxy: Identifier

    def to_dict(self) -> dict:
        """Converts Class into dictionary."""
        return {
            "PatientIdentifier": {
                "IdentifierValue": self.patient.value,
                "IdentifierType": self.patient.type,
            },
            "PatientNationalPracticeCode": self.patient_ods_code,
            "UserIdentifier": {
                "IdentifierValue": self.proxy.value,
                "IdentifierType": self.proxy.type,
            },
        }


class SessionRequestHeaders(BaseModel):
    """Base Model for the request headers required to create a session."""

    application_id: str
    version: str = "1"

    def to_dict(self) -> dict:
        """Converts Class into dictionary."""
        return {
            "X-API-ApplicationId": self.application_id,
            "X-API-Version": self.version,
        }


class MedicalRecordPermissions(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    record_access_scheme: str
    allergies_enabled: bool
    consultations_enabled: bool
    immunisations_enabled: bool
    documents_enabled: bool
    medication_enabled: bool
    problems_enabled: bool
    test_results_enabled: bool


class Permissions(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    appointments_enabled: bool
    demographics_update_enabled: bool
    eps_enabled: bool
    medical_record_enabled: bool
    online_triage_enabled: bool
    practice_patient_communication_enabled: bool
    prescribing_enabled: bool
    record_sharing_enabled: bool
    record_view_audit_enabled: bool
    medical_record: MedicalRecordPermissions


class Patient(Demographics):
    permissions: Permissions


class SessionResponse(ForwardResponse):
    model_config = ConfigDict(alias_generator=to_camel)

    end_user_session_id: str
    patients: list[Patient]
