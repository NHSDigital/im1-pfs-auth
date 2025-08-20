from pydantic import BaseModel


class Demographics(BaseModel):
    """A data model that encapsulates all the essential demographic data."""

    first_name: str
    surname: str
    title: str


class ForwardResponse(BaseModel):
    """A data model that encapsulates all the essential information needed to forward a external backend system response to the client."""  # noqa: E501

    session_id: str
    supplier: str
    proxy: Demographics
    patients: list[Demographics]
