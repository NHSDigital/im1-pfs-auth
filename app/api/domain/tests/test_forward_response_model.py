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
                    accessSystemConnect=True,
                    bookAppointments=True,
                    changePharamacy=True,
                    messagePractice=True,
                    provideInformationToPractice=True,
                    requestMedication=True,
                    updateDemographics=True,
                    manageOnlineTriage=True,
                    view=ViewPermissions(
                        medicalRecord=False,
                        summaryMedicalRecord=False,
                        allergiesMedicalRecord=False,
                        consultationsMedicalRecord=False,
                        immunisationsMedicalRecord=False,
                        documentsMedicalRecord=False,
                        medicationMedicalRecord=False,
                        problemsMedicalRecord=False,
                        testResultsMedicalRecord=False,
                        recordAudit=False,
                        recordSharing=False,
                    ),
                ),
            )
        ],
    )
