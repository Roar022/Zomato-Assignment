import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import json

import chromadb
chroma_client = chromadb.PersistentClient(path="cromadb_storage")
chroma_client.heartbeat()

collection = chroma_client.get_or_create_collection(
    name="zomato",
    metadata={"description": "A food and resturant guide."}
)

documents = []
metadatas = []

def generate_chunks(restaurants):
    for r in restaurants:
        restId = r.get('id', 'none')
        name = r.get('name', 'Unknown')
        location = r.get('location', 'Unknown')
        contact = r.get('contact', {})
        phone = contact.get('phone', 'N/A')
        hours = r.get('operating_hours', {})
        weekday_hours = hours.get('mon-fri', 'N/A')
        weekend_hours = hours.get('sat-sun', 'N/A')

        for item in r.get('menu', []):
            dish = item.get('name', 'Unnamed dish')
            desc = item.get('description', '').strip()
            features = item.get('features', [])
            if not desc:
                continue

            text = f"{dish} is served at {name} having description as follows: {desc}"
            documents.append(text)

            metadata = {
                "restaurant_id": str(restId),
                "restaurant_name": name,
                "dish_name": dish,
                "description": desc,
                "price": float(item.get('price', 0)) if item.get('price') else 0,
                "dietary": ", ".join(item.get('dietary', [])),
                "operating_hours": f"Weekdays - {weekday_hours} Weekends - {weekend_hours}",
                "features": ", ".join(features),
                "contact": phone,
                "available": True if item.get('available') else False,
            }
            metadatas.append(metadata)

with open("restaurants.json", "r", encoding="utf-8") as f:
    restaurant_data = json.load(f)

generate_chunks(restaurant_data)


model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def getembeddings(texts):
    if isinstance(texts, str):
        texts = [texts]
    embeddings = model.encode(
        texts,
        show_progress_bar=False,
        convert_to_numpy=True,
    )
    return embeddings.tolist()


query_text = "What food can i have at dominos?"
query_embedding = getembeddings(query_text)

results = collection.query(
    query_embeddings=query_embedding,
    n_results=15,
    include=["documents", "metadatas", "distances"]
)
print(results)
print("Query Results:")
for doc, meta, dist in zip(results["documents"][0], results["metadatas"][0], results["distances"][0]):
    print(f"- Document: {doc}\n  Metadata: {meta}\n  Distance: {dist}\n")
