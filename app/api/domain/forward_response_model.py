from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class Demographics(BaseModel):
    """A data model that encapsulates all the essential demographic data."""

    model_config = ConfigDict(alias_generator=to_camel)

    first_name: str
    surname: str
    title: str


class ForwardResponse(BaseModel):
    """A data model that encapsulates all the essential information needed to forward a external backend system response to the client."""  # noqa: E501

    model_config = ConfigDict(alias_generator=to_camel)

    session_id: str
    end_user_session_id: str
    supplier: str
    proxy: Demographics
    patients: list[Demographics]
