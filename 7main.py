from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import RateUpdateRequest, VehicleEntryRequest, PaymentRequest, OverrideEntryRequest
from tariff_manager import tariff_service
from entry_module import entry_service
from exit_module import exit_calculator
from payment_module import payment_service
from reporting_module import reporting_service

app = FastAPI(title="Modern Automated Parking System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/display/live")
def get_live_display():
    return entry_service.get_display_status()

@app.get("/api/admin/tariff")
def get_tariff():
    return tariff_service.get_current_tariff()

@app.post("/api/admin/tariff")
def update_tariff(payload: RateUpdateRequest):
    return tariff_service.update_tariff(
        payload.base_rate, payload.hourly_rate, payload.grace_period_minutes, payload.vat_percentage
    )

@app.post("/api/entry/record")
def record_entry(payload: VehicleEntryRequest):
    res = entry_service.process_entry(payload.plate_number)
    if not res["success"]:
        raise HTTPException(status_code=400, detail=res["message"])
    return res

@app.get("/api/exit/calculate/{plate_number}")
def calculate_exit(plate_number: str):
    plate_key = plate_number.strip().upper()
    if plate_key not in entry_service.active_sessions:
        raise HTTPException(status_code=404, detail=f"No active session found for plate {plate_key}")
    
    session_data = entry_service.active_sessions[plate_key]
    return exit_calculator.calculate_fee(session_data)

@app.post("/api/exit/pay")
def process_checkout(payload: PaymentRequest):
    session_data = None
    for plate, session in list(entry_service.active_sessions.items()):
        if session["session_id"] == payload.session_id:
            session_data = session
            break

    if not session_data:
        raise HTTPException(status_code=404, detail="Session not found")

    calc_res = exit_calculator.calculate_fee(session_data)
    pay_res = payment_service.process_payment(
        session_data, calc_res, payload.payment_method, payload.amount_paid, payload.mpesa_receipt_number
    )

    if not pay_res["success"]:
        raise HTTPException(status_code=400, detail=pay_res["message"])

    plate_key = session_data["plate_number"]
    bay_key = session_data["bay_number"]
    
    del entry_service.active_sessions[plate_key]
    entry_service.bays[bay_key]["is_occupied"] = False
    entry_service.bays[bay_key]["plate"] = None
    entry_service.available_slots += 1

    return pay_res

@app.post("/api/admin/override-exit")
def handle_unrecorded_exit(payload: OverrideEntryRequest):
    net = round(payload.flat_rate / 1.16, 2)
    vat = round(payload.flat_rate - net, 2)
    
    override_record = {
        "transaction_id": len(payment_service.transactions) + 5001,
        "session_id": 9999,
        "plate_number": payload.plate_number.upper(),
        "bay_number": "UNRECORDED",
        "net_amount": net,
        "vat_amount": vat,
        "gross_amount": payload.flat_rate,
        "payment_method": "CASH_OVERRIDE",
        "mpesa_receipt": payload.reason,
        "payment_time": "OVERRIDE"
    }
    payment_service.transactions.append(override_record)
    return {"success": True, "barrier_signal": "OPEN", "record": override_record}

@app.get("/api/admin/reports/vat")
def get_vat_report():
    return reporting_service.generate_vat_reconciliation_report(payment_service.transactions)
