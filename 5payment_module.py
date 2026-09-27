from datetime import datetime


class PaymentController:
    def __init__(self):
        self.transactions = []

    def process_payment(self, session_data: dict, calculation: dict, method: str, amount_paid: float, mpesa_receipt: str = None) -> dict:
        valid_methods = ["MPESA", "CARD", "CASH"]
        method_upper = method.upper()

        if method_upper not in valid_methods:
            return {"success": False, "message": f"Invalid method. Choose from {valid_methods}"}

        if amount_paid < calculation["gross_payable"]:
            return {"success": False, "message": f"Insufficient payment. Required: {calculation['gross_payable']}"}

        transaction_record = {
            "transaction_id": len(self.transactions) + 5001,
            "session_id": session_data["session_id"],
            "plate_number": session_data["plate_number"],
            "bay_number": session_data["bay_number"],
            "net_amount": calculation["net_amount"],
            "vat_amount": calculation["vat_amount"],
            "gross_amount": calculation["gross_payable"],
            "payment_method": method_upper,
            "mpesa_receipt": mpesa_receipt if method_upper == "MPESA" else "N/A",
            "payment_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        self.transactions.append(transaction_record)

        return {
            "success": True,
            "barrier_signal": "OPEN",
            "message": "Payment verified. Exit barrier released.",
            "transaction": transaction_record
        }
    

payment_service = PaymentController()