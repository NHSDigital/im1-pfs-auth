from app.api.domain.forward_response_model import Demographics, ForwardResponse


def test_forward_response() -> None:
    """Tests the ForwardResponse model."""
    # Act & Assert
    ForwardResponse(
        sessionId="some session id",
        supplier="some supplier",
        proxy=Demographics(firstName="Betty", surname="Jones", title="Ms"),
        patients=[Demographics(firstName="John", surname="Jones", title="Mr")],
    )
