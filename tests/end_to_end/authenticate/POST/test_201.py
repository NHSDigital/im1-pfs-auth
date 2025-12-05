"""All tests in this file are for the 201 OK response."""

from logging import getLogger
from uuid import uuid4

import pytest
from requests import post

from tests.end_to_end.utils.apigee_authentication import get_authentication_token

logger = getLogger(__name__)


@pytest.mark.positive
@pytest.mark.parametrize(
    ("forward_to_url", "expected_response"),
    [
        (
            "https://emis.com",
            {
                "patients": [
                    {
                        "firstName": "Alex",
                        "surname": "Taylor",
                        "title": "Mr",
                        "permissions": {
                            "accessSystemConnect": False,
                            "bookAppointments": True,
                            "changePharmacy": True,
                            "manageOnlineTriage": False,
                            "messagePractice": False,
                            "provideInformationToPractice": False,
                            "requestMedication": True,
                            "updateDemographics": True,
                            "view": {
                                "allergiesMedicalRecord": True,
                                "consultationsMedicalRecord": True,
                                "documentsMedicalRecord": True,
                                "immunisationsMedicalRecord": True,
                                "medicalRecord": True,
                                "medicationMedicalRecord": True,
                                "problemsMedicalRecord": True,
                                "recordAudit": True,
                                "recordSharing": False,
                                "summaryMedicalRecord": True,
                                "testResultsMedicalRecord": True,
                            },
                        },
                    },
                    {
                        "firstName": "Jane",
                        "surname": "Doe",
                        "title": "Mrs",
                        "permissions": {
                            "accessSystemConnect": False,
                            "bookAppointments": False,
                            "changePharmacy": True,
                            "manageOnlineTriage": True,
                            "messagePractice": True,
                            "provideInformationToPractice": True,
                            "requestMedication": True,
                            "updateDemographics": True,
                            "view": {
                                "allergiesMedicalRecord": True,
                                "consultationsMedicalRecord": True,
                                "documentsMedicalRecord": True,
                                "immunisationsMedicalRecord": True,
                                "medicalRecord": True,
                                "medicationMedicalRecord": True,
                                "problemsMedicalRecord": True,
                                "recordAudit": True,
                                "recordSharing": False,
                                "summaryMedicalRecord": True,
                                "testResultsMedicalRecord": True,
                            },
                        },
                    },
                    {
                        "firstName": "Ella",
                        "surname": "Taylor",
                        "title": "Ms",
                        "permissions": {
                            "accessSystemConnect": False,
                            "bookAppointments": True,
                            "changePharmacy": False,
                            "manageOnlineTriage": False,
                            "messagePractice": True,
                            "provideInformationToPractice": True,
                            "requestMedication": False,
                            "updateDemographics": True,
                            "view": {
                                "allergiesMedicalRecord": True,
                                "consultationsMedicalRecord": True,
                                "documentsMedicalRecord": True,
                                "immunisationsMedicalRecord": True,
                                "medicalRecord": True,
                                "medicationMedicalRecord": True,
                                "problemsMedicalRecord": True,
                                "recordAudit": True,
                                "recordSharing": False,
                                "summaryMedicalRecord": True,
                                "testResultsMedicalRecord": True,
                            },
                        },
                    },
                ],
                "proxy": {"firstName": "Alex", "surname": "Taylor", "title": "Mr"},
                "sessionId": "SID_2qZ9yJpVxHq4N3b",
                "supplier": "EMIS",
            },
        ),
        (
            "https://tpp.com",
            {
                "patients": [
                    {
                        "firstName": "Clare",
                        "surname": "Jones",
                        "title": "Mrs",
                        "permissions": {
                            "accessSystemConnect": False,
                            "bookAppointments": True,
                            "changePharmacy": False,
                            "manageOnlineTriage": False,
                            "messagePractice": True,
                            "provideInformationToPractice": False,
                            "requestMedication": True,
                            "updateDemographics": False,
                            "view": {
                                "allergiesMedicalRecord": True,
                                "consultationsMedicalRecord": False,
                                "documentsMedicalRecord": False,
                                "immunisationsMedicalRecord": False,
                                "medicalRecord": False,
                                "medicationMedicalRecord": True,
                                "problemsMedicalRecord": False,
                                "recordAudit": True,
                                "recordSharing": False,
                                "summaryMedicalRecord": True,
                                "testResultsMedicalRecord": False,
                            },
                        },
                    },
                ],
                "proxy": {"firstName": "Sam", "surname": "Jones", "title": "Mr"},
                "sessionId": "xhvE9/jCjdafytcXBq8LMKMgc4wA/w5k/O5C4ip0Fs9GPbIQ/WRIZi4Och1Spmg7aYJR2CZVLHfu6cRVv84aEVrRE8xahJbT4TPAr8N/CYix6TBquQsZibYXYMxJktXcYKwDhBH8yr3iJYnyevP3hV76oTjVmKieBtYzSSZAOu4=",  # noqa: E501
                "supplier": "TPP",
            },
        ),
    ],
)
def test_happy_path(
    request: pytest.FixtureRequest,
    api_url: str,
    forward_to_url: str,
    expected_response: dict,
) -> None:
    """Test the happy path for the API.

    Test Scenario:
        Given: API is ready
        When: a valid request is made with correct parameters
        Then: the response status code is 201
        And: the response body contains the expected data

    """
    # Arrange
    uuid = str(uuid4())
    proxy_identifier = "9912003071"  # P9 User with composite token
    headers = {
        "Authorization": get_authentication_token(proxy_identifier, request),
        "X-Application-ID": request.node.name,
        "X-Request-ID": uuid,
        "X-Forward-To": forward_to_url,
        "X-ODS-Code": "ODS123",
        "X-Correlation-ID": uuid,
    }
    # Act
    response = post(api_url, headers=headers, timeout=5)
    # Assert
    assert response.status_code == 201
    assert response.json() == expected_response
