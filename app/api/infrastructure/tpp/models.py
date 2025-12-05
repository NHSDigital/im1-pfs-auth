from uuid import uuid4

from pydantic import BaseModel


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
