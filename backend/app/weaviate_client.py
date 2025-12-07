# app/weaviate_client.py
import weaviate
from weaviate.classes.config import Configure, Property, DataType

class WeaviateHandler:
    def __init__(self, host="localhost", port=8080):
        self.client = weaviate.connect_to_local(host=host, port=port)
        self.collection_name = "Documents"
        self._ensure_collection()

    def _ensure_collection(self):
        collections = self.client.collections.list_all()
        if self.collection_name not in collections:
            print("Creating Weaviate collection...")
            self.client.collections.create(
                name=self.collection_name,
                properties=[
                    Property(name="html", data_type=DataType.TEXT),
                    Property(name="text", data_type=DataType.TEXT),
                    Property(name="summary", data_type=DataType.TEXT)
                ],
                vectorizer_config=Configure.Vectorizer.none()
            )
            
    def reset_collection(self):
        collections = self.client.collections.list_all()
        if self.collection_name in collections:
            self.client.collections.delete(self.collection_name)

        self._ensure_collection()

    def add_document(self, html: str, text: str, summary: str, embedding):
        collection = self.client.collections.get(self.collection_name)
        collection.data.insert(
            properties={
                "html": html,
                "text": text,
                "summary": summary
            },
            vector=embedding
        )
    def search(self, query_embedding: list, limit: int = 10):
        collection = self.client.collections.get(self.collection_name)

        results = collection.query.near_vector(
            near_vector=query_embedding,
            limit=limit,
            return_properties=["html", "text", "summary"],
            return_metadata=["score"]     # <-- IMPORTANT
        )

        final = []
        for item in results.objects:
            score = item.metadata.score      # <-- FIXED (always present)
            relevance = round(score * 100, 2)

            final.append({
                "html": item.properties["html"],
                "text": item.properties["text"],
                "summary": item.properties["summary"],
                "relevance": relevance
            })

        return final
