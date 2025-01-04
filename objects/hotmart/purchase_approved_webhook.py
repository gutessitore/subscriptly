from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    has_co_production: bool
    name: str
    id: int
    ucode: str

class Commission(BaseModel):
    source: str
    value: float
    currency_value: str

class Offer(BaseModel):
    code: str

class Price(BaseModel):
    currency_value: str
    value: float

class CheckoutCountry(BaseModel):
    iso: str
    name: str

class OrderBump(BaseModel):
    is_order_bump: bool

class Payment(BaseModel):
    installments_number: int
    type: str

class Purchase(BaseModel):
    offer: Offer
    order_date: int
    original_offer_price: Price
    price: Price
    checkout_country: CheckoutCountry
    order_bump: OrderBump
    payment: Payment
    approved_date: int
    full_price: Price
    transaction: str
    status: str
    invoice_by: Optional[str]
    subscription_anticipation_purchase: Optional[bool]
    date_next_charge: Optional[int]
    recurrence_number: Optional[int]

class Affiliate(BaseModel):
    affiliate_code: str
    name: str

class Producer(BaseModel):
    name: str

class Subscriber(BaseModel):
    code: str

class Plan(BaseModel):
    name: str
    id: int

    @property
    def is_quarterly(self):
        return 'trimestral' in self.name.lower()

class Subscription(BaseModel):
    subscriber: Subscriber
    plan: Plan
    status: str

class Buyer(BaseModel):
    name: str
    checkout_phone: str
    email: str
    address: Optional[dict]
    document: Optional[str]

class Data(BaseModel):
    product: Product
    commissions: list[Commission]
    purchase: Purchase
    affiliates: list[Affiliate]
    producer: Producer
    subscription: Subscription
    buyer: Buyer

class PurchaseApprovedResponse(BaseModel):
    data: Data
    id: str
    creation_date: int
    event: str
    version: str
