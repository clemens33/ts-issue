import asyncio
from typing import List

import aiohttp
import pandas as pd
import requests
from aiohttp import ClientTimeout


def inference_backend(backend: str,
                      queries: List[str],
                      timeout: float = 0.1,
                      limit: int = 100,  # concurrent requests
                      ) -> List[dict]:
    timeout = int(len(queries) * timeout)

    async def fetch(session, query):
        async with session.post(backend, json={"query": query}) as response:
            response = await response.json(content_type=None)

            return response

    async def fetch_all():
        connector = aiohttp.TCPConnector(limit=limit)
        async with aiohttp.ClientSession(connector=connector, timeout=ClientTimeout(total=timeout)) as session:
            tasks = []

            for query in queries:
                tasks.append(
                    fetch(session, query)
                )

            responses = await asyncio.gather(*tasks, return_exceptions=True)

            return responses

    # responses = asyncio.run(fetch_all()) from python 3.7 onwards
    loop = asyncio.get_event_loop()
    responses = loop.run_until_complete(fetch_all())

    return responses


if __name__ == "__main__":
    file_name = "test_queries.csv"
    column_name = "query"
    model_name = "dummy"
    nr_requests = 1000000
    limit = 1000

    backend = "http://localhost:8080" + "/predictions/" + model_name
    response = requests.get(backend)
    assert response.status_code == 200, f"backend {backend} for predictions and model {model_name} not reachable"

    df = pd.read_csv(file_name, usecols=[column_name])
    df = df.iloc[:nr_requests]

    # queries = [str(uuid.uuid4()) for _ in range(len(df))]
    queries = df[column_name].tolist()
    print(f"number of queries: {len(queries)}")

    responses = inference_backend(backend, queries, limit=limit)

    for idx, response in enumerate(responses):
        if isinstance(response, dict) and "results" in response:
            pass
        else:
            print(f"idx: {str(idx)} / query: {queries[idx]} / response: {response}")

    assert len(queries) == len(responses)
