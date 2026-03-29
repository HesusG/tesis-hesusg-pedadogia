"""Translate downloaded Chinese policy documents to English via Together.ai."""

import time
import sys
from pathlib import Path
from openai import OpenAI
from config import (
    TOGETHER_API_BASE, TOGETHER_API_KEY, PRIMARY_MODEL, FALLBACK_MODEL,
    TRANSLATION_TEMPERATURE, DOWNLOADS_DIR, TRANSLATIONS_DIR, POLICY_DOCUMENTS,
)

client = OpenAI(base_url=TOGETHER_API_BASE, api_key=TOGETHER_API_KEY)

CHUNK_SIZE = 4000  # chars per chunk
SYSTEM_PROMPT = (
    "You are a professional translator specializing in Chinese government policy documents. "
    "Translate the following Chinese text into English faithfully and accurately. "
    "Preserve the original document structure, paragraph breaks, and numbering. "
    "Use standard English terminology for Chinese government institutions and policies. "
    "Do not add commentary or interpretation. Translate only."
)


def chunk_text(text: str, max_chars: int = CHUNK_SIZE) -> list[str]:
    """Split text into chunks at paragraph boundaries."""
    paragraphs = text.split("\n\n")
    chunks = []
    current = ""

    for para in paragraphs:
        if len(current) + len(para) + 2 > max_chars and current:
            chunks.append(current.strip())
            current = para
        else:
            current = current + "\n\n" + para if current else para

    if current.strip():
        chunks.append(current.strip())

    return chunks


def translate_chunk(text: str, model: str) -> str:
    """Translate a single chunk of text."""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ],
        temperature=TRANSLATION_TEMPERATURE,
        max_tokens=4096,
    )
    return response.choices[0].message.content


def translate_text(text: str) -> str:
    """Translate full document text, chunking as needed. Try primary model, fall back."""
    chunks = chunk_text(text)
    translated_chunks = []

    for i, chunk in enumerate(chunks):
        if not chunk.strip():
            continue

        print(f"    Chunk {i+1}/{len(chunks)} ({len(chunk)} chars)...", end=" ", flush=True)

        # Try primary model
        try:
            result = translate_chunk(chunk, PRIMARY_MODEL)
            print(f"OK ({PRIMARY_MODEL.split('/')[-1]})")
            translated_chunks.append(result)
            time.sleep(2)
            continue
        except Exception as e:
            print(f"Primary failed: {e}")

        # Try fallback model
        try:
            print(f"    Retrying with {FALLBACK_MODEL}...", end=" ", flush=True)
            result = translate_chunk(chunk, FALLBACK_MODEL)
            print("OK")
            translated_chunks.append(result)
            time.sleep(2)
        except Exception as e:
            print(f"Fallback also failed: {e}")
            translated_chunks.append(f"[TRANSLATION FAILED FOR CHUNK {i+1}]\n{chunk[:200]}...")

    return "\n\n".join(translated_chunks)


def main():
    if not TOGETHER_API_KEY:
        print("ERROR: TOGETHER_API_KEY not set in .env")
        sys.exit(1)

    print("=" * 60)
    print("Translating policy documents")
    print("=" * 60)

    results = []
    for doc in POLICY_DOCUMENTS:
        doc_id = doc["id"]
        slug = doc["slug"]
        title = doc["title"]

        txt_path = DOWNLOADS_DIR / f"{doc_id}_{slug}.txt"
        if not txt_path.exists():
            print(f"\n[{doc_id}/7] SKIP (not downloaded): {title}")
            results.append((title, False))
            continue

        text = txt_path.read_text(encoding="utf-8")
        chinese_chars = sum(1 for c in text if "\u4e00" <= c <= "\u9fff")
        if chinese_chars < 50:
            print(f"\n[{doc_id}/7] SKIP (too few Chinese chars: {chinese_chars}): {title}")
            results.append((title, False))
            continue

        print(f"\n[{doc_id}/7] Translating: {title} ({len(text)} chars)")

        translated = translate_text(text)
        out_path = TRANSLATIONS_DIR / f"{doc_id}_{slug}_en.txt"
        out_path.write_text(translated, encoding="utf-8")

        print(f"  Saved: {out_path.name} ({len(translated)} chars)")
        results.append((title, True))

    print("\n" + "=" * 60)
    print("Translation Summary")
    print("=" * 60)
    for title, success in results:
        status = "OK" if success else "SKIP"
        print(f"  [{status}] {title}")

    success_count = sum(1 for _, s in results if s)
    print(f"\n{success_count}/{len(results)} documents translated")


if __name__ == "__main__":
    main()
