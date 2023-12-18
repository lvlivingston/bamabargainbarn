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
    # Get the order and mark it as paid
    order_id = session.get('client_reference_id')
    order = get_object_or_404(Order, id=order_id)
    order.paid = True
    order.save()