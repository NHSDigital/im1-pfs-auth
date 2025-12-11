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
                            "appointmentsEnabled": True,
                            "demographicsUpdateEnabled": True,
                            "epsEnabled": True,
                            "medicalRecordEnabled": True,
                            "onlineTriageEnabled": False,
                            "practicePatientCommunicationEnabled": False,
                            "prescribingEnabled": True,
                            "recordSharingEnabled": False,
                            "recordViewAuditEnabled": True,
                            "medicalRecord": {
                                "recordAccessScheme": "DetailedCodedCareRecord",
                                "allergiesEnabled": True,
                                "consultationsEnabled": True,
                                "immunisationsEnabled": True,
                                "documentsEnabled": True,
                                "medicationEnabled": True,
                                "problemsEnabled": True,
                                "testResultsEnabled": True,
                            },
                        },
                    },
                    {
                        "firstName": "Jane",
                        "surname": "Doe",
                        "title": "Mrs",
                        "permissions": {
                            "appointmentsEnabled": False,
                            "demographicsUpdateEnabled": True,
                            "epsEnabled": False,
                            "medicalRecordEnabled": True,
                            "onlineTriageEnabled": True,
                            "practicePatientCommunicationEnabled": True,
                            "prescribingEnabled": True,
                            "recordSharingEnabled": False,
                            "recordViewAuditEnabled": True,
                            "medicalRecord": {
                                "recordAccessScheme": "CoreSummaryCareRecord",
                                "allergiesEnabled": True,
                                "consultationsEnabled": True,
                                "immunisationsEnabled": True,
                                "documentsEnabled": True,
                                "medicationEnabled": True,
                                "problemsEnabled": True,
                                "testResultsEnabled": True,
                            },
                        },
                    },
                    {
                        "firstName": "Ella",
                        "surname": "Taylor",
                        "title": "Ms",
                        "permissions": {
                            "appointmentsEnabled": True,
                            "demographicsUpdateEnabled": True,
                            "epsEnabled": False,
                            "medicalRecordEnabled": True,
                            "onlineTriageEnabled": False,
                            "practicePatientCommunicationEnabled": True,
                            "prescribingEnabled": False,
                            "recordSharingEnabled": False,
                            "recordViewAuditEnabled": True,
                            "medicalRecord": {
                                "recordAccessScheme": "DetailedCodedCareRecord",
                                "allergiesEnabled": True,
                                "consultationsEnabled": True,
                                "immunisationsEnabled": True,
                                "documentsEnabled": True,
                                "medicationEnabled": True,
                                "problemsEnabled": True,
                                "testResultsEnabled": True,
                            },
                        },
                    },
                ],
                "proxy": {"firstName": "Alex", "surname": "Taylor", "title": "Mr"},
                "sessionId": "SID_2qZ9yJpVxHq4N3b",
                "endUserSessionId": "SESS_mDq6nE2b8R7KQ0v",
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
                        "permissions": [
                            {
                                "description": "Full Clinical Record",
                                "statusDescription": "Unavailable",
                                "serviceIdentifier": 1,
                                "status": "U",
                            },
                            {
                                "serviceIdentifier": 2,
                                "statusDescription": "Available",
                                "description": "Appointments",
                                "status": "A",
                            },
                            {
                                "serviceIdentifier": 4,
                                "statusDescription": "Available",
                                "description": "Request Medication",
                                "status": "A",
                            },
                            {
                                "serviceIdentifier": 8,
                                "description": "Questionnaires",
                                "status": "N",
                                "statusDescription": "Not offered by unit",
                            },
                            {
                                "serviceIdentifier": 64,
                                "statusDescription": "Available",
                                "description": "Summary Record",
                                "status": "A",
                            },
                            {
                                "serviceIdentifier": 128,
                                "statusDescription": "Unavailable",
                                "description": "Detailed Coded Record",
                                "status": "U",
                            },
                            {
                                "serviceIdentifier": 512,
                                "statusDescription": "Available",
                                "description": "Messaging",
                                "status": "A",
                            },
                            {
                                "serviceIdentifier": 1024,
                                "statusDescription": "Not offered by unit",
                                "description": "View Sharing Status",
                                "status": "N",
                            },
                            {
                                "serviceIdentifier": 2048,
                                "statusDescription": "Available",
                                "description": "Record Audit",
                                "status": "A",
                            },
                            {
                                "serviceIdentifier": 4096,
                                "statusDescription": "Not offered by unit",
                                "description": "Change Pharmacy",
                                "status": "N",
                            },
                            {
                                "serviceIdentifier": 8192,
                                "statusDescription": (
                                    "Only available to GMS registered patients"
                                ),
                                "description": "Manage Sharing Rules And Requests",
                                "status": "G",
                            },
                            {
                                "serviceIdentifier": 65536,
                                "statusDescription": "Other",
                                "description": "Access SystmConnect",
                                "status": "O",
                            },
                        ],
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
        "X-Use-Mock": "True",
    }
    # Act
    response = post(api_url, headers=headers, timeout=5)
    # Assert
    assert response.status_code == 201
    assert response.json() == expected_response
