from app.api.domain.forward_response_model import Demographics, ForwardResponse


def test_forward_response() -> None:
    """Tests the ForwardResponse model."""
    # Act & Assert
    ForwardResponse(
        session_id="some session",
        supplier="some supplier",
        proxy=Demographics(first_name="Betty", surname="Jones", title="Ms"),
        patients=[Demographics(first_name="John", surname="Jones", title="Mr")],
    )
