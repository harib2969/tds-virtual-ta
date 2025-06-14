import os
import json
import openai
from dotenv import load_dotenv
from utils.helpers import chunk_text

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("AIPROXY_TOKEN")
openai.api_base = os.getenv("OPENAI_API_BASE", "https://aiproxy.sanand.workers.dev/openai")
embedding_model = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

# Input and output paths
input_path = "data/discourse_posts.json"
output_path = "data/embeddings.json"

# Load discourse posts
with open(input_path, "r", encoding="utf-8") as f:
    posts = json.load(f)

embeddings_data = []

for post in posts:
    text = post.get("title", "") + "\n" + post.get("content", "")
    chunks = chunk_text(text, max_tokens=800)  # chunk helper will split if too long

    for i, chunk in enumerate(chunks):
        try:
            print(f"🔹 Embedding post ID {post['id']} chunk {i+1}/{len(chunks)}")
            response = openai.embeddings.create(
                model=embedding_model,
                input=chunk
            )
            embedding = response.data[0].embedding
            embeddings_data.append({
                "post_id": post["id"],
                "chunk_index": i,
                "text": chunk,
                "embedding": embedding
            })
        except Exception as e:
            print(f"❌ Failed to embed post ID {post['id']} chunk {i}: {e}")

# Save embeddings
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(embeddings_data, f, indent=2)

print(f"✅ Embeddings saved to {output_path}")
