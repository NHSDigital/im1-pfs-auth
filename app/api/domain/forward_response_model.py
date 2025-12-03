from pydantic import BaseModel, ConfigDict, field_validator
from pydantic.alias_generators import to_camel


class Demographics(BaseModel):
    """A data model that encapsulates all the essential demographic data."""

    model_config = ConfigDict(alias_generator=to_camel)

    first_name: str
    surname: str
    title: str


class ViewPermissions(BaseModel):
    """All the view permissions data the proxy holds for a pateint."""

    medical_record: bool  # tpp = coded_medical_record
    summary_medical_record: bool  # EMIS view medical record
    allergies_medical_record: bool  # tpp summary
    consultations_medical_record: bool  # tpp coded
    immunisations_medical_record: bool  # tpp coded
    documents_medical_record: bool  # tpp coded
    medication_medical_record: bool  # tpp summary
    problems_medical_record: bool  # tpp coded
    test_results_medical_record: bool  # tpp coded
    record_audit: bool
    record_sharing: bool  # thes come back to


class Permissions(BaseModel):
    """All the permissions data a proxy holds for a patient."""

    access_system_connect: bool  # tpp only
    book_appointments: bool
    change_pharamacy: bool
    messsage_practice: bool
    provide_information_to_practice: (
        bool  # tpp questionnaires emis patient practice communications
    )
    request_medication: bool
    update_demographics: bool  # emis only
    manage_online_triage: (
        bool  # for tpp is system connect, questionnaires and messaging
    )
    view: ViewPermissions


class Patient(Demographics):
    """Patient data model that extends Demographics with the addition of permissions."""

    permissions: Permissions


class ForwardResponse(BaseModel):
    """All the essential information needed to forward a external backend system response to the client."""  # noqa: E501

    model_config = ConfigDict(alias_generator=to_camel)

    session_id: str
    supplier: str
    proxy: Demographics
    patients: list[Patient]

    @field_validator("patients")
    def patients_must_not_be_empty(cls, v):
        if not v:
            raise ValueError("patients cannot be empty")
        return v
