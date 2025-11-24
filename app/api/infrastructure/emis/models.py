from pydantic import BaseModel


class Identifier(BaseModel):
    """Base Model for identifiers."""
    value: str
    type: str = "NhsNumber"


class CreateSessionRequestData(BaseModel):
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


class CreateSessionRequestHeaders(BaseModel):
    """Base Model for the request headers required to create a session."""
    application_id: str
    version: str = "1"

    def to_dict(self) -> dict:
        """Converts Class into dictionary."""
        return {
            "X-API-ApplicationId": self.application_id,
            "X-API-Version": self.version,
        }
