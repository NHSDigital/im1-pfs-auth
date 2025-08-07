from pydantic import BaseModel


class Demographics(BaseModel):
    """A data model that encapsulates all the essential demographic data"""

    first_name: str
    surname: str
    title: str


class ForwardResponse(Demographics):
    """A data model that encapsulates all the essential information needed to forward a external backend system response to the client"""

    session_id: str
    patients: list[Demographics]
