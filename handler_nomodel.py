import logging
import os
import sys
from argparse import Namespace
from typing import List, Dict

from ts.torch_handler.base_handler import BaseHandler

logger = logging.getLogger(__name__)

logger.info(f"loaded modules: {dir()}")
logger.info(f"pid: {os.getpid()}")
logger.info(f"oscwd: {os.getcwd()}")
logger.info(f"ppid: {os.getppid()}")
logger.info(f"interpreter: {sys.executable}")


class Handler(BaseHandler):

    def __init__(self):
        super(Handler, self).__init__()

        self.initialized = False

    def initialize(self, ctx):
        self.manifest = ctx.manifest

        self.initialized = True

    def _preprocess(self, requests) -> List[str]:
        # logger.info(f"raw requests {requests}")

        queries = []
        for data in requests:
            # logger.info(f"data-type: {type(data)} / data: {data}")

            if isinstance(data, dict):
                data = data.get("body") if "body" in data else data

            if isinstance(data, (bytes, bytearray)):
                data = data.decode("utf-8")

                query = data
            else:
                # handle application/json request - envelope body
                query = data["query"]

            queries.append(query)

        logger.info(f"number of requests captured: {len(queries)}")

        return queries

    def preprocess(self, requests):
        queries = self._preprocess(requests)

        return {
            "queries": queries,
        }

    def inference(self, inputs, *args, **kwargs):
        return {
            "queries": inputs["queries"]
        }

    def _postprocess(self, outputs: Dict) -> List[Dict]:
        """create some problematic dummy responses"""

        dummy_responses = []

        # # simple return seams to be no problem
        # for query in outputs["queries"]:
        #     dummy_responses.append({
        #         "query": query,
        #         "results": ["dummy_class" + str(k) for k in range(3)]
        #     })

        # complex response seams to sometimes crash workers with io.netty.handler.codec.DecoderException: java.lang.IndexOutOfBoundsException: readerIndex(....
        for query in outputs["queries"]:
            dummy_responses.append({
                "query": query,
                "results": [{
                    "dummy_class" + str(k): 0.01,
                    "dummy_entry1": {
                        "stuff1": 1,
                        "stuff2": 2,
                        "stuff3": 3,
                        "stuff4": 4,
                        "stuff5": {
                            "explain1": 0.1,
                            "explain2": 0.1,
                        }
                    }
                } for k in range(3)]
            })

        return dummy_responses

    def postprocess(self, inference_output):
        return self._postprocess(inference_output)


# local handler test without torchserve
if __name__ == "__main__":
    requests = [
        {
            "query": "first request captured",
        },
        {
            "query": "the european super league is not so super",
        }
    ]

    ctx = Namespace(**{
        "manifest": {
            "model": {
                "serializedFile": "dummy.ckpt",
            }
        },
        "system_properties": {
            "model_dir": ".",
            "gpu_id": 0,
        }
    })

    handler = Handler()
    handler.initialize(ctx)

    inputs = handler.preprocess(requests)
    results = handler.inference(inputs)
    response = handler.postprocess(results)

    print(response)

    assert len(requests) == len(response)
