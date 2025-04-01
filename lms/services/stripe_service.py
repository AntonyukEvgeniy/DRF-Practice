from typing import Dict, Optional

import requests
from environs import Env

env = Env()
env.read_env()


STRIPE_API_KEY = env.str("STRIPE_SECRET_API_KEY")
STRIPE_API_URL = "https://api.stripe.com/v1"


class StripeService:
    def __init__(self):
        self.api_key = STRIPE_API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

    def create_product(self, name: str, description: Optional[str] = None) -> Dict:
        """
        Создает новый продукт в Stripe
        """
        url = f"{STRIPE_API_URL}/products"
        data = {"name": name, "description": description}

        response = requests.post(url, headers=self.headers, data=data)
        return response.json()

    def create_price(
        self, product_id: str, unit_amount: int, currency: str = "usd"
    ) -> Dict:
        """
        Создает новую цену для продукта в Stripe
        :param product_id: ID продукта в Stripe
        :param unit_amount: Стоимость в минимальных единицах валюты (центы для USD)
        :param currency: Валюта (по умолчанию USD)
        """
        url = f"{STRIPE_API_URL}/prices"
        data = {"product": product_id, "unit_amount": unit_amount, "currency": currency}

        response = requests.post(url, headers=self.headers, data=data)
        return response.json()

    def create_payment_link_session(
        self, course_id: str, price_id: str, success_url: str, cancel_url: str
    ) -> Dict:
        """
        Создает сессию оплаты в Stripe
        """
        url = f"{STRIPE_API_URL}/checkout/sessions"
        data = {
            "payment_method_types[]": "card",
            "line_items[][price]": price_id,
            "line_items[][quantity]": 1,
            "mode": "payment",
            "success_url": success_url,
            "cancel_url": cancel_url,
            "metadata[course_id]": course_id,
        }

        response = requests.post(url, headers=self.headers, data=data)
        return response.json()
