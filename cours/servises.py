import stripe
import constants

stripe.api_key = constants.STRIPE_API_KEY


def pay_link(product_name, product_cost):
    product = stripe.Product.create(
        name=product_name
    )
    price = stripe.Price.create(
        unit_amount=product_cost * 100,
        currency="rub",
        recurring={"interval": "month"},
        product=product.id,
    )
    session = stripe.checkout.Session.create(
        success_url="https://example.com/success",
        line_items=[
            {
                "price": price.id,
                "quantity": 1,
            },
            ],
        mode="subscription",
    )

    return session.url


