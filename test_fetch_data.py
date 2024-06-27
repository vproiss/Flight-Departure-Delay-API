import unittest
from unittest.mock import patch
from fetch_data import fetch_data

class TestFetchData(unittest.TestCase):
    """
    Unit tests for "fetch_data.py".
    """

    @patch('fetch_data.requests.get')
    def test_fetch_data(self, mock_get):
        """
        Test the fetch_data function if it correctly processes the flight schedule and delay data.

        Args:
            mock_get: Mocked requests.get method to control the data being returned.
        """
        # Mock the schedule response.
        mock_schedule_response = {
            "FlightStatusResource": {
                "Flights": {
                    "Flight": [
                        {
                            "OperatingCarrier": {
                                "FlightNumber": "203",
                                "AirlineID": "OS"
                            },
                            "Departure": {
                                "AirportCode": "VIE",
                                "ScheduledTimeUTC": {"DateTime": "2024-06-19T06:00Z"},
                                "ActualTimeUTC": {"DateTime": "2024-06-19T06:05Z"},
                                "Gate": "3",
                                "Terminal": {"Name": "1"}
                            },
                            "Arrival": {
                                "AirportCode": "FRA",
                                "Gate": "1",
                                "Terminal": {"Name": "2"}
                            },
                            "FlightStatus": {"Definition": "Flight Landed"},
                            "Equipment": {"AircraftCode": "320"}
                        }
                    ]
                }
            }
        }

        # Mock the delay response.
        mock_delay_response = [
            {
                "Flight": {
                    "OperatingFlight": {
                        "Number": "203",
                        "Airline": "OS"
                    }
                },
                "FlightLegs": [
                    {
                        "Departure": {
                            "Delay": {
                                "Code1": {"Code": "93", "DelayTime": 20, "Description": "Aircraft Rotation"},
                                "Code2": {"Code": "7", "DelayTime": 10, "Description": "Cabin Baggage"}
                            }
                        }
                    }
                ]
            }
        ]

        # Setup the mock response for the requests.get calls.
        mock_get.side_effect = [
            unittest.mock.Mock(ok=True, json=lambda: mock_schedule_response),
            unittest.mock.Mock(ok=True, json=lambda: mock_delay_response)
        ]

        result = fetch_data()

        # Check the results.
        self.assertEqual(len(result), 1)
        flight = result[0]
        self.assertEqual(flight['flight_number'], "203")
        self.assertEqual(flight['airline'], "OS")
        self.assertEqual(flight['origin'], "VIE")
        self.assertEqual(flight['destination'], "FRA")
        self.assertEqual(flight['scheduled_departure_at'], "2024-06-19T06:00Z")
        self.assertEqual(flight['actual_departure_at'], "2024-06-19T06:05Z")
        self.assertEqual(flight['status'], "Flight Landed")
        self.assertEqual(flight['aircraft_type'], "320")
        self.assertEqual(flight['departure_gate'], "3")
        self.assertEqual(flight['arrival_gate'], "1")
        self.assertEqual(flight['departure_terminal'], "1")
        self.assertEqual(flight['arrival_terminal'], "2")
        self.assertEqual(len(flight['delays']), 2)
        self.assertEqual(flight['delays'][0]['code'], "93")
        self.assertEqual(flight['delays'][0]['time_minutes'], 20)
        self.assertEqual(flight['delays'][0]['description'], "Aircraft Rotation")
        self.assertEqual(flight['delays'][1]['code'], "7")
        self.assertEqual(flight['delays'][1]['time_minutes'], 10)
        self.assertEqual(flight['delays'][1]['description'], "Cabin Baggage")

if __name__ == '__main__':
    unittest.main()





