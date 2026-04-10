from app.api.domain.forward_response_model import (
    Demographics,
    ForwardResponse,
    Permissions,
)


def test_forward_response() -> None:
    """Tests the ForwardResponse model."""
    # Act & Assert
    ForwardResponse(
        sessionId="some session id",
        supplier="some supplier",
        odsCode="some ods code",
        user=Demographics(
            firstName="Betty",
            surname="Jones",
            title="Ms",
            dateOfBirth="12/03/1965",
            permissions=Permissions(),
        ),
        patients=[
            Demographics(
                firstName="John",
                surname="Jones",
                title="Mr",
                dateOfBirth="18/05/1966",
                permissions=Permissions(),
            ),
        ],
    )
