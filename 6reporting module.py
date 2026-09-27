from datetime import datetime


class ReportingService:
    def generate_vat_reconciliation_report(self, transactions: list) -> dict:
        total_gross = 0.0
        total_net = 0.0
        total_vat = 0.0
        method_breakdown = {"MPESA": 0.0, "CARD": 0.0, "CASH": 0.0}

        for txn in transactions:
            total_gross += txn["gross_amount"]
            total_net += txn["net_amount"]
            total_vat += txn["vat_amount"]
            method = txn["payment_method"]
            if method in method_breakdown:
                method_breakdown[method] += txn["gross_amount"]

        return {
            "report_generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_transactions": len(transactions),
            "summary": {
                "total_gross_revenue": round(total_gross, 2),
                "total_net_revenue": round(total_net, 2),
                "total_vat_collected_16pct": round(total_vat, 2)
            },
            "payment_method_breakdown": method_breakdown,
            "audit_trail": transactions
        }
    

reporting_service = ReportingService()