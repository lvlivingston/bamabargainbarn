import stripe
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Set your Stripe API key from the environment variable
stripe.api_key = os.environ.get("STRIPE_API_KEY")

stripe.PaymentLink.create(
    line_items=[
        {
            "price": '{{PRICE_ID}}', 
            "quantity": 1, 
            "adjustable_quantity": {"enabled": True, "minimum": 1, "maximum": 10}
        },
    ],
    billing_address_collection="required",
    shipping_address_collection={"allowed_countries": ["US"]},
    shipping_options=[{"shipping_rate": '{{SHIPPING_RATE_ID}}'}],
    allow_promotion_codes=True,
    payment_method_types=["card"],
    automatic_tax={"enabled": True},
    after_completion={"type": "redirect", "redirect": {"url": "https://example.com"}},
)

stripe.Price.create(
    currency="usd",
    unit_amount=1000,
    product='{{PRODUCT_ID}}',
)