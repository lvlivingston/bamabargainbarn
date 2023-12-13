import stripe
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Set your Stripe API key from the environment variable
stripe.api_key = os.environ.get("STRIPE_API_KEY")

# Ensure the API key is set
if stripe.api_key is None:
    raise ValueError("Stripe API key is not set. Make sure to set the STRIPE_API_KEY environment variable.")

starter_subscription = stripe.Product.create(
  name="Starter Subscription",
  description="$12/Month subscription",
)

starter_subscription_price = stripe.Price.create(
  unit_amount=1200,
  currency="usd",
  recurring={"interval": "month"},
  product=starter_subscription['id'],
)

# Save these identifiers
print(f"Success! Here is your starter subscription product id: {starter_subscription.id}")
print(f"Success! Here is your starter subscription price id: {starter_subscription_price.id}")