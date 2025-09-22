from fastapi.testclient import TestClient
from src.main import api, tickets

client = TestClient(api)


def setup_function():
    """Clear tickets list before each test (avoid test data leaking)."""
    tickets.clear()


def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Message": "Welcome to the Ticket Booking System"}


def test_add_ticket():
    ticket_data = {
        "id": 1,
        "flight_name": "AirTest",
        "flight_date": "2025-10-15",
        "flight_time": "14:30",
        "destination": "New York",
    }
    response = client.post("/ticket", json=ticket_data)
    assert response.status_code == 200
    assert response.json() == ticket_data
    assert len(tickets) == 1


def test_get_tickets():
    # Add one first
    ticket_data = {
        "id": 1,
        "flight_name": "AirTest",
        "flight_date": "2025-10-15",
        "flight_time": "14:30",
        "destination": "New York",
    }
    client.post("/ticket", json=ticket_data)

    response = client.get("/ticket")
    assert response.status_code == 200
    assert response.json() == [ticket_data]


def test_update_ticket():
    ticket_data = {
        "id": 1,
        "flight_name": "AirTest",
        "flight_date": "2025-10-15",
        "flight_time": "14:30",
        "destination": "New York",
    }
    client.post("/ticket", json=ticket_data)

    updated_ticket = {
        "id": 1,
        "flight_name": "AirUpdated",
        "flight_date": "2025-11-20",
        "flight_time": "15:45",
        "destination": "London",
    }
    response = client.put("/ticket/1", json=updated_ticket)
    assert response.status_code == 200
    assert response.json() == updated_ticket
    assert tickets[0].flight_name == "AirUpdated"


def test_delete_ticket():
    ticket_data = {
        "id": 1,
        "flight_name": "AirTest",
        "flight_date": "2025-10-15",
        "flight_time": "14:30",
        "destination": "New York",
    }
    client.post("/ticket", json=ticket_data)

    response = client.delete("/ticket/1")
    assert response.status_code == 200
    assert response.json() == ticket_data
    assert len(tickets) == 0


def test_delete_ticket_not_found():
    response = client.delete("/ticket/99")
    assert response.status_code == 200
    assert response.json() == {"error": "Ticket not found, deletion failed"}
