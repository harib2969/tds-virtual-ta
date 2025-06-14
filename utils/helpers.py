import tiktoken

def chunk_text(text, max_tokens=500):
    enc = tiktoken.encoding_for_model("text-embedding-ada-002")
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        current_chunk.append(word)
        tokens = enc.encode(" ".join(current_chunk))
        if len(tokens) > max_tokens:
            current_chunk.pop()
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks
