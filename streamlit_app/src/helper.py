# src/utils.py

import json
import chromadb
from chromadb.config import Settings
from .config import client, LLM, EMBEDDING_MODEL
from .prompt import PROMPT
from sentence_transformers import SentenceTransformer

class ZomatoBot:
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        self.chroma_client = chromadb.PersistentClient(path="cromadb_storage")
        self.collection = self.chroma_client.get_or_create_collection(
            name="zomato",
            metadata={"description": "A food and restaurant guide."}
        )
        self.chroma_client.heartbeat()

    def generate_embeddings(self, texts):
        if isinstance(texts, str):
            texts = [texts]
        embeddings = self.model.encode(
            texts,
            show_progress_bar=False,
            convert_to_numpy=True,
        )
        return embeddings.tolist()

    def search_similar_context(self, query: str, top_k: int = 15):
        query_embedding = self.generate_embeddings(query)
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )
        meta_data = []
        for doc, meta, dist in zip(results["documents"][0], results["metadatas"][0], results["distances"][0]):
            meta_data.append(meta)
        return meta_data

    def generate_reply(self, messages: list, user_query: str) -> str:
        context = self.search_similar_context(user_query)

        if not any(m["role"] == "system" for m in messages):
            messages.append({
                "role": "system",
                "content": PROMPT
            })

        messages.append({
            "role": "system",
            "content": f"{context}"
        })
        messages.append({
            "role": "user",
            "content": user_query
        })

        chat_completion = client.chat.completions.create(
            model=LLM,
            messages=messages
        )

        assistant_reply = chat_completion.choices[0].message.content

        messages.append({
            "role": "assistant",
            "content": assistant_reply
        })

        return assistant_reply
