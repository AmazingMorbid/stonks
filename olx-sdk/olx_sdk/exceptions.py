
class OfferNotFound(Exception):
    def __init__(self, offer_id: int):
        super(OfferNotFound, self).__init__(f"Offer with specified id={offer_id} not found.")
