from requests import Response

from .base_client import BaseClient
from domain.forward_response_model import ForwardResponse


class TppClient(BaseClient):
    """An implementation of BaseClient tailored for forwarding requests to TPP's backend"""

    def get_headers(self):
        return {
            "X-API-ApplicationId": self.request.application_id,  # The identity of the subsidiary
            "X-API-Version": "1",  # "The version of the API requested"
        }

    def get_data(self):
        return {
            "patientId": self.request.patient_nhs_number,
            "onlineUserId": self.request.proxy_nhs_number,
            "unitId": self.request.patient_ods_code,
        }

    def transform_response(self, response: Response) -> ForwardResponse:
        return super().transform_response(response)
