from mongoengine import (
    Document,
    StringField,
    DateTimeField,
    DecimalField,
    ObjectIdField
)
from datetime import datetime

CURRENCY_CHOICES = ['USD', 'INR', 'EUR']


class Auction(Document):
    item_name = StringField(required=True)
    start_time = DateTimeField(required=True, default=datetime.utcnow)
    end_time = DateTimeField(required=True)
    start_price = DecimalField(required=True)
    highest_bid = DecimalField()
    currency_string = StringField(required=True, choices=CURRENCY_CHOICES)
    user_id = ObjectIdField(required=False, default=None)
    meta = {'collection': "Auctions"}



