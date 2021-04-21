import asyncio
import json
import string
import random
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime, timedelta

import requests

from common import schemas


def put(session, id):
    url = "http://localhost:8000/offers"
    offer = schemas.Offer(id=id,
                          title="".join(random.choice(string.ascii_letters) for _ in range(20)),
                          description="".join(random.choice(string.ascii_letters) for _ in range(20)),
                          url="https://example.org",
                          price=random.randint(1, 2000),
                          last_refresh_time=datetime.now() - timedelta(minutes=random.randint(0, 5000)),
                          last_scraped_time=datetime.now() - timedelta(minutes=random.randint(0, 2000)))
    with session.put(url, data=json.dumps(offer.dict(), default=str)) as response:
        return response.json()


async def put_data_async():
    ids_to_put = [i for i in range(500000)]

    with ThreadPoolExecutor(max_workers=10) as executor:
        with requests.Session() as session:
            loop = asyncio.get_event_loop()

            tasks = [
                loop.run_in_executor(
                    executor,
                    put,
                    *(session, id)
                )
                for id in ids_to_put
            ]

            for response in await asyncio.gather(*tasks):
                pass


def main():
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(put_data_async())
    loop.run_until_complete(future)


main()
