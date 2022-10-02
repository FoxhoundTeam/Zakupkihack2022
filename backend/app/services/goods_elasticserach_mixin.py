from functools import cached_property
from typing import TYPE_CHECKING

from elasticsearch import Elasticsearch

from app.config import settings

if TYPE_CHECKING:
    from app.database import Good

GOODS_MAPPING = {
    "mappings": {
        "properties": {
            "complete_name": {"type": "completion"},
            "name": {"type": "text"},
            "description": {"type": "text"},
        }
    }
}


class GoodsElasticsearchMixin:
    index = "goods"

    @cached_property
    def es(self) -> Elasticsearch:
        es = Elasticsearch(hosts=[settings.elasticsearch_server])
        es.indices.create(index=self.index, body=GOODS_MAPPING, ignore=400)
        return es

    def es_autocomplete(self, pattern: str) -> list[str]:
        return [
            option["text"]
            for option in self.es.search(
                index=self.index,
                suggest={
                    "completion_suggest": {
                        "prefix": pattern,
                        "completion": {
                            "field": "complete_name",
                            "size": 10,
                            "skip_duplicates": True,
                            "fuzzy": {"fuzziness": 1, "prefix_length": 1},
                        },
                    }
                },
            )["suggest"]["completion_suggest"][0]["options"]
        ]

    def es_create_good(self, good: "Good"):
        self.es.index(
            index=self.index,
            id=good.id,
            document={"name": good.name, "complete_name": good.name, "description": good.description},
        )
        self.es.indices.refresh(index=self.index)

    def es_get_ids_by_q(self, q: str) -> list[int]:
        return [
            int(match["_id"])
            for match in self.es.search(
                index=self.index,
                query={
                    "multi_match": {
                        "query": q,
                        "fields": ["name", "description"],
                        "fuzziness": 2,
                    }
                },
            )["hits"]["hits"]
        ]
