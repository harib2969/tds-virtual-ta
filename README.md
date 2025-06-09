# tds-virtual-ta
Virtual Teaching Assistant that automatically answers student questions using content from the TDS Jan 2025 course and Discourse posts.

This project is a Virtual Teaching Assistant API that answers student questions using:

- Course content from the **Tools in Data Science (TDS)** course (Jan 2025)
- Posts from the TDS Discourse forum (1 Jan 2025 – 14 Apr 2025)

## Features

- Scrapes course and forum content
- Uses embeddings to find relevant posts
- Exposes a FastAPI endpoint to answer questions using OpenAI GPT
- Returns relevant Discourse links in each response

## API Usage

Send a `POST` request to the `/api/` endpoint with:

```json
{
  "question": "Your question here",
  "image": "Base64-encoded image (optional)"
}
