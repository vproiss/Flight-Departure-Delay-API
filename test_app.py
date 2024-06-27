import unittest
from unittest.mock import patch
from app import app, update_data

class AppTestCase(unittest.TestCase):
    """
    Unit tests for the Flask application.
    """

    @patch('app.fetch_data')
    def setUp(self, mock_fetch_data):
        """
        Set up the test client and mock data for testing.

        Args:
            mock_fetch_data: Mocked fetch_data function to control the data being returned.
        """
        # Mock fetch_data to control the data being returned.
        mock_fetch_data.return_value = [
            {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "flight_number": "2325",
                "airline": "LH",
                "origin": "VIE",
                "destination": "MUC",
                "scheduled_departure_at": "2024-06-19T10:05",
                "actual_departure_at": "2024-06-19T10:39",
                "status": "Flight Landed",
                "aircraft_type": "320",
                "departure_gate": "G1",
                "arrival_gate": "G2",
                "departure_terminal": "T1",
                "arrival_terminal": "T2",
                "delays": [
                    {
                        "code": "34",
                        "time_minutes": 20,
                        "description": "Late arrival of aircraft"
                    }
                ]
            },
            {
                "id": "223e4567-e89b-12d3-a456-426614174000",
                "flight_number": "2325",
                "airline": "LH",
                "origin": "VIE",
                "destination": "MUC",
                "scheduled_departure_at": "2024-06-19T10:05",
                "actual_departure_at": "2024-06-19T10:39",
                "status": "Flight Landed",
                "aircraft_type": "320",
                "departure_gate": "G1",
                "arrival_gate": "G2",
                "departure_terminal": "T1",
                "arrival_terminal": "T2",
                "delays": [
                    {
                        "code": "34",
                        "time_minutes": 20,
                        "description": "Late arrival of aircraft"
                    }
                ]
            }
        ]
        # Create a test client for the Flask application.
        self.app = app.test_client()
        self.app.testing = True
        update_data()

    def test_home(self):
        """
        Test the home page.
        """
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Flight Data', response.data)

    def test_get_flights(self):
        """
        Test the /api/flights endpoint without filters.
        """
        response = self.app.get('/api/flights')
        self.assertEqual(response.status_code, 200)
        flights = response.get_json()
        self.assertEqual(len(flights), 1)
        self.assertEqual(flights[0]['flight_number'], "2325")

    def test_get_flights_with_filter(self):
        """
        Test the /api/flights endpoint with filters.
        """
        response = self.app.get('/api/flights?destination=MUC')
        self.assertEqual(response.status_code, 200)
        flights = response.get_json()
        self.assertEqual(len(flights), 1)
        self.assertEqual(flights[0]['destination'], "MUC")

        response = self.app.get('/api/flights?airline=LH')
        self.assertEqual(response.status_code, 200)
        flights = response.get_json()
        self.assertEqual(len(flights), 1)
        self.assertEqual(flights[0]['airline'], "LH")

    def test_get_destinations(self):
        """
        Test the /api/destinations endpoint.
        """
        response = self.app.get('/api/destinations')
        self.assertEqual(response.status_code, 200)
        destinations = response.get_json()
        self.assertIn("MUC", destinations)

    def test_get_airlines(self):
        """
        Test the /api/airlines endpoint.
        """
        response = self.app.get('/api/airlines')
        self.assertEqual(response.status_code, 200)
        airlines = response.get_json()
        self.assertIn("LH", airlines)

if __name__ == '__main__':
    unittest.main()




