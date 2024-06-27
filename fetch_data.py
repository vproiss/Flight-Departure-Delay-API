import pandas as pd
import uuid
import requests

# URLs to get the flight schedule and delay data.
FLIGHT_SCHEDULE_URL = "https://challenge.usecosmos.cloud/flight_schedules.json"
FLIGHT_DELAY_URL = "https://challenge.usecosmos.cloud/flight_delays.json"

def fetch_data():
    """
    This fucniton gets the flight schedule and delay data, processes it, and returns a list of flight records.

    Returns:
        list: A list of dictionaries, each containing flight information and associated delays.
    """
    try:
        schedule_response = requests.get(FLIGHT_SCHEDULE_URL)
        schedule_response.raise_for_status()
        schedules_raw = schedule_response.json()['FlightStatusResource']['Flights']['Flight']

        delay_response = requests.get(FLIGHT_DELAY_URL)
        delay_response.raise_for_status()
        delays_raw = delay_response.json()

        # Process the flight schedules.
        schedules = []
        for flight in schedules_raw:
            schedule = {
                "flight_number": flight['OperatingCarrier']['FlightNumber'],
                "airline": flight['OperatingCarrier']['AirlineID'],
                "origin": flight['Departure']['AirportCode'],
                "destination": flight['Arrival']['AirportCode'],
                "scheduled_departure_at": flight['Departure']['ScheduledTimeUTC']['DateTime'],
                "actual_departure_at": flight['Departure']['ActualTimeUTC']['DateTime'],
                "status": flight['FlightStatus']['Definition'],
                "aircraft_type": flight['Equipment']['AircraftCode'],
                "departure_gate": flight['Departure'].get('Gate'),
                "arrival_gate": flight['Arrival'].get('Gate'),
                "departure_terminal": flight['Departure'].get('Terminal', {}).get('Name'),
                "arrival_terminal": flight['Arrival'].get('Terminal', {}).get('Name')
            }
            schedules.append(schedule)
        
        schedules_df = pd.DataFrame(schedules)

        # Process the flight delays.
        delays_dict = {}
        for flight in delays_raw:
            flight_info = flight['Flight']
            flight_key = (flight_info['OperatingFlight']['Number'], flight_info['OperatingFlight']['Airline'])
            if flight_key not in delays_dict:
                delays_dict[flight_key] = []
            for leg in flight['FlightLegs']:
                delay_info = leg['Departure']['Delay']
                if delay_info.get('Code1'):
                    delays_dict[flight_key].append({
                        "code": delay_info['Code1']['Code'],
                        "time_minutes": delay_info['Code1']['DelayTime'],
                        "description": delay_info['Code1']['Description']
                    })
                if delay_info.get('Code2'):
                    delays_dict[flight_key].append({
                        "code": delay_info['Code2']['Code'],
                        "time_minutes": delay_info['Code2']['DelayTime'],
                        "description": delay_info['Code2']['Description']
                    })
                if delay_info.get('Code3'):
                    delays_dict[flight_key].append({
                        "code": delay_info['Code3']['Code'],
                        "time_minutes": delay_info['Code3']['DelayTime'],
                        "description": delay_info['Code3']['Description']
                    })
                if delay_info.get('Code4'):
                    delays_dict[flight_key].append({
                        "code": delay_info['Code4']['Code'],
                        "time_minutes": delay_info['Code4']['DelayTime'],
                        "description": delay_info['Code4']['Description']
                    })
        
        # Merge the schedules and delays.
        result = []
        for _, row in schedules_df.iterrows():
            flight_key = (row['flight_number'], row['airline'])
            delays = delays_dict.get(flight_key, [])
            result.append({
                "id": str(uuid.uuid4()),
                "flight_number": row['flight_number'],
                "airline": row['airline'],
                "origin": row['origin'],
                "destination": row['destination'],
                "scheduled_departure_at": row['scheduled_departure_at'],
                "actual_departure_at": row['actual_departure_at'],
                "status": row['status'],
                "aircraft_type": row['aircraft_type'],
                "departure_gate": row['departure_gate'],
                "arrival_gate": row['arrival_gate'],
                "departure_terminal": row['departure_terminal'],
                "arrival_terminal": row['arrival_terminal'],
                "delays": delays
            })
        
        return result
    
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []





















