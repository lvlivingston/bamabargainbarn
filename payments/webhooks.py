from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.conf import settings
from main_app.models import Customer, Product, Order, OrderItem
import stripe
from datetime import timedelta
from django.utils import timezone

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_ENDPOINT_SECRET
        )
        print(f"Webhook Event: {event}")
    except ValueError as e:
        # Invalid payload
        return JsonResponse({'error: invalid payload': str(e)}, status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return JsonResponse({'error: invalid signature': str(e)}, status=400)

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        handle_payment_success(session)

    return JsonResponse({'status': 'successful payment'})

def handle_payment_success(session):
    try:
        # Get the order and mark it as paid
        order_id = session.get('client_reference_id')
        order = get_object_or_404(Order, id=order_id)
        price_with_shipping = order.price_with_shipping  # Use the order's price_with_shipping
        # Update the price_paid field
        order.price_paid = price_with_shipping
        order.paid = True
        # Capture and update email and phone
        order.email = session.get('customer_email', '')  # use 'customer_email' from Stripe
        order.phone = session.get('customer_phone', '')  # use 'customer_phone' from Stripe
        order.save()

        print(f"Order {order_id} marked as paid successfully. Price Paid: {price_with_shipping}")
    except Exception as e:
        print(f"Error marking order as paid: {e}")