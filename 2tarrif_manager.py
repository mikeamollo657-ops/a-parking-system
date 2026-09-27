from datetime import datetime


class TariffManager:
    def __init__(self):
        self._tariff = {
            "base_rate": 50.0,
            "hourly_rate": 100.0,
            "grace_period_minutes": 15,
            "vat_percentage": 16.0,
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def get_current_tariff(self) -> dict:
        return self._tariff

    def update_tariff(self, base_rate: float, hourly_rate: float, grace_period_minutes: int, vat_percentage: float) -> dict:
        self._tariff = {
            "base_rate": base_rate,
            "hourly_rate": hourly_rate,
            "grace_period_minutes": grace_period_minutes,
            "vat_percentage": vat_percentage,
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return self._tariff
    

tariff_service = TariffManager()
