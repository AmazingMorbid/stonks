from stonks_api import models
from stonks_api.database import SessionLocal

session = SessionLocal()

# offer = models.OlxOffer(id=123,
#                         title="test offer",
#                         description="test offer description",
#                         price=69)
#
# session.add(offer)
# session.commit()

new_offer = models.Offer(id=1234,
                         title="test offer",
                         description="test offer description",
                         price=69)

session.merge(new_offer)
session.commit()
