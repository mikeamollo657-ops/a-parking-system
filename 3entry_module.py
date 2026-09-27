from datetime import datetime
from threading import Lock

class EntryController:
    def __init__(self, total_capacity: int = 20):
        self.total_capacity = total_capacity
        self.available_slots = total_capacity
        self.lock = Lock()
        self.bays = {f"BAY-{i:02d}": {"is_occupied": False, "plate": None} for i in range(1, total_capacity + 1)}
        self.active_sessions = {}
        self.session_counter = 1000

    def get_display_status(self)-> dict:
        return {
            "total_capacity": self.total_capacity,
            "available_slots": self.available_slots,
            "status": "OPEN" if self.available_slots > 0 else "FULL"
        }

    def process_entry(self, plate_number: str) -> dict:
        plate_key = plate_number.strip().upper()

        with self.lock:
            if self.available_slots <= 0:
                return {"success": False, "message": "ENTRY DENIED: Parking Lot Full"}

            if plate_key in self.active_sessions:
                return {"success": False, "message": f"ENTRY DENIED: Vehicle {plate_key} is already parked"}

            allocated_bay = None
            for bay_id, info in self.bays.items():
                if not info["is_occupied"]:
                    allocated_bay = bay_id
                    info["is_occupied"] = True
                    info["plate"] = plate_key
                    break

            if not allocated_bay:
                return {"success": False, "message": "ENTRY DENIED: No Bay Available"}

            self.session_counter += 1
            session_id = self.session_counter
            entry_time = datetime.now()

            self.active_sessions[plate_key] = {
                "session_id": session_id,
                "plate_number": plate_key,
                "bay_number": allocated_bay,
                "entry_time": entry_time,
                "is_override": False
            }

            self.available_slots -= 1

            return {
                "success": True,
                "barrier_signal": "OPEN",
                "session_id": session_id,
                "plate_number": plate_key,
                "allocated_bay": allocated_bay,
                "entry_time": entry_time.strftime("%Y-%m-%d %H:%M:%S"),
                "available_slots": self.available_slots
            }

entry_service = EntryController()

