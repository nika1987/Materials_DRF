import uuid

import stripe

from config.settings import STRIPE_API_KEY

API_KEY = STRIPE_API_KEY


def generate_payment_id():
    return str(uuid.uuid4())


def get_session(payment):
    """Функция возвращает сессию для оплаты"""
    stripe.api_key = API_KEY

    product = stripe.Product.create(
        name=payment.name
    )

    price = stripe.Price.create(
        currency='eur',
        unit_amount=payment.price_amount,
        product=product.id
    )

    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[
            {
                'price': price.id,
                'quantity': 1,
            }
        ],
        mode='payment'
    )

    return session.url

# def create_stripe_price(payment):
#    stripe.api_key = API_KEY

#   stripe_product = stripe.Product.create(
#       name=payment.paid_course.name
#   )

#   stripe_price = stripe.Price.create(
#       currency="rub",
#       unit_amount=payment.payment_amount * 100,
#       product_data={"name": stripe_product.name}
#   )

#   return stripe_price.id


# def create_stripe_session(stripe_price_id):
#   stripe.api_key = API_KEY
#    stripe_session = stripe.checkout.Session.create(
#       line_items=[{
#           'price': stripe_price_id,
#           'quantity': 1
#       }],
#       mode='payment',
#       success_url='https://example.com/success'
#   )
#
#   return stripe_session.url, stripe_session.id
