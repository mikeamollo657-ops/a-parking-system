import math
from datetime import datetime
from tariff_manager import tariff_service


class FeeCalculator:
    def calculate_fee(self, session_data: dict) -> dict:
        entry_time = session_data["entry_time"]
        exit_time = datetime.now()
        
        duration_seconds = (exit_time - entry_time).total_seconds()
        duration_minutes = duration_seconds / 60.0
        
        tariff = tariff_service.get_current_tariff()
        
        if duration_minutes <= tariff["grace_period_minutes"]:
            gross_payable = 0.0
            duration_hours = 0
        else:
            duration_hours = math.ceil(duration_seconds / 3600.0)
            gross_payable = tariff["base_rate"] + (duration_hours * tariff["hourly_rate"])

        vat_rate = tariff["vat_percentage"] / 100.0
        net_amount = round(gross_payable / (1.0 + vat_rate), 2)
        vat_amount = round(gross_payable - net_amount, 2)

        return {
            "session_id": session_data["session_id"],
            "plate_number": session_data["plate_number"],
            "bay_number": session_data["bay_number"],
            "entry_time": entry_time.strftime("%Y-%m-%d %H:%M:%S"),
            "exit_time": exit_time.strftime("%Y-%m-%d %H:%M:%S"),
            "duration_hours": duration_hours,
            "net_amount": net_amount,
            "vat_amount": vat_amount,
            "gross_payable": round(gross_payable, 2)
        }
    

exit_calculator = FeeCalculator()
