### booking/models.py

from typing import TypedDict
from datetime import date
from decimal import Decimal

class BookingReservation(TypedDict):
    id: str
    checkin: date
    checkout: date
    property_id: int
    property_name: str
    rooms: list[dict[str, int | str]] | None
    booked_date: date
    guest_name: str
    adults: int
    children: list[int, list[int]] | None
    total_price: Decimal
    fee: Decimal
    currency: str
    status: str

    @classmethod
    def as_json(cls, reservation: "BookingReservation") -> dict[str, str | int | list]:
        return {
            "id": reservation["id"],
            "checkin": reservation["checkin"].isoformat(),
            "checkout": reservation["checkout"].isoformat(),
            "property_id": reservation["property_id"],
            "property_name": reservation["property_name"],
            "rooms": reservation["rooms"],
            "booked_date": reservation["booked_date"].isoformat(),
            "guest_name": reservation["guest_name"],
            "adults": reservation["adults"],
            "children": reservation["children"],
            "total_price": str(reservation["total_price"]),
            "fee": str(reservation["fee"]),
            "currency": reservation["currency"],
            "status": reservation["status"],
        }