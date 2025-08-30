from fastapi import APIRouter, Form

router = APIRouter(prefix="/ussd", tags=["ussd"]) 


@router.post("/")
async def ussd_webhook(
	sessionId: str = Form(...),
	serviceCode: str = Form(...),
	phoneNumber: str = Form(...),
	text: str = Form("")
):
	# Simple demo USSD flow: 1) Book a ride 2) Check status
	if text == "":
		response = "CON SafiriSchola\n1. Book Ride\n2. Check Status"
	elif text == "1":
		response = "CON Enter Child ID"
	elif text.startswith("1*") and len(text.split("*")) == 2:
		response = "CON Enter Pickup Location"
	elif text.startswith("1*") and len(text.split("*")) == 3:
		response = "CON Enter Dropoff Location"
	elif text.startswith("1*") and len(text.split("*")) >= 4:
		# In production we would persist booking and send SMS
		response = "END Ride request received. You will get an SMS shortly."
	elif text == "2":
		response = "END Status: No active rides."
	else:
		response = "END Invalid selection"
	return response