import stripe
from ..config import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(amount, booking_id):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "inr",
                    "product_data": {"name": f"Booking #{booking_id}"},
                    "unit_amount": amount * 100,  # amount in paise
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=f"http://localhost:8000/payments/success?booking_id={booking_id}",
        cancel_url="http://localhost:8000/payments/cancel",
    )
    return session
