from app.api.domain.forward_response_model import (
    Demographics,
    ForwardResponse,
    Patient,
    Permissions,
    ViewPermissions,
)


def test_forward_response() -> None:
    """Tests the ForwardResponse model."""
    # Act & Assert
    ForwardResponse(
        sessionId="some session id",
        supplier="some supplier",
        proxy=Demographics(firstName="Betty", surname="Jones", title="Ms"),
        patients=[
            Patient(
                firstName="John",
                surname="Jones",
                title="Mr",
                permissions=Permissions(
                    access_system_connect=True,
                    book_appointments=True,
                    change_pharamacy=True,
                    messsage_practice=True,
                    provide_information_to_practice=True,
                    request_medication=True,
                    update_demographics=True,
                    manage_online_triage=True,
                    view=ViewPermissions(
                        medical_record=False,
                        summary_medical_record=False,
                        allergies_medical_record=False,
                        consultations_medical_record=False,
                        immunisations_medical_record=False,
                        documents_medical_record=False,
                        medication_medical_record=False,
                        problems_medical_record=False,
                        test_results_medical_record=False,
                        record_audit=False,
                        record_sharing=False,
                    ),
                ),
            )
        ],
    )
