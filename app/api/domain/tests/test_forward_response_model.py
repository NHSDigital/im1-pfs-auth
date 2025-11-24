from app.api.domain.forward_response_model import Demographics, ForwardResponse


def test_forward_response() -> None:
    """Tests the ForwardResponse model."""
    # Act & Assert
    ForwardResponse(
        session_id="some session id",
        end_user_session_id="some end user session id",
        supplier="some supplier",
        proxy=Demographics(first_name="Betty", surname="Jones", title="Ms"),
        patients=[Demographics(first_name="John", surname="Jones", title="Mr")],
    )
