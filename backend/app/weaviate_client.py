# app/weaviate_client.py
import weaviate
from weaviate.classes.config import Configure, Property, DataType

class WeaviateHandler:
    def __init__(self, host="localhost", port=8080):
        # Connect to local Weaviate instance
        self.client = weaviate.connect_to_local(host=host, port=port)
        self.collection_name = "Documents"
        self._ensure_collection()

    def _ensure_collection(self):
        """Create collection if it doesn't exist"""
        collections = self.client.collections.list_all()
        if self.collection_name not in collections:
            print("Creating Weaviate collection...")
            self.client.collections.create(
                name=self.collection_name,
                properties=[Property(name="text", data_type=DataType.TEXT)],
                vectorizer_config=Configure.Vectorizer.none()
            )

    def add_document(self, text: str, embedding):
        """Insert a document with vector (convert numpy array to list if needed)"""
        if hasattr(embedding, "tolist"):
            embedding = embedding.tolist()

        collection = self.client.collections.get(self.collection_name)
        collection.data.insert(
            properties={"text": text},
            vector=embedding
        )

    def search(self, query_embedding: list, limit: int = 10):
        collection = self.client.collections.get(self.collection_name)
        results = collection.query.near_vector(
            near_vector=query_embedding,
            limit=limit
        )

        seen = set()
        unique_results = []
        for item in results.objects:
            text = item.properties["text"]
            if text not in seen:
                unique_results.append(text)
                seen.add(text)
        return unique_results[:limit]

