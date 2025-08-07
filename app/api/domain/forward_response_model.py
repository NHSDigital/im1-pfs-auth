from pydantic import BaseModel, field_validator


class ForwardResponse(BaseModel):
    """A domain-level data model that encapsulates all the essential information needed to forward a external backend system response to the client"""
