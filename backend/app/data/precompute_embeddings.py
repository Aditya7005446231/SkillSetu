"""Precompute all-MiniLM-L6-v2 embeddings for skill_framework.json using ONNX and numpy."""
import json
from pathlib import Path
import numpy as np
import onnxruntime as ort
from tokenizers import Tokenizer

DATA_DIR = Path(__file__).resolve().parent
FRAMEWORK_PATH = DATA_DIR / "skill_framework.json"
MODEL_DIR = DATA_DIR / "models" / "all-MiniLM-L6-v2"
EMBEDDINGS_PATH = DATA_DIR / "skill_embeddings.npy"
METADATA_PATH = DATA_DIR / "skill_metadata.json"

def compute_embeddings():
    print(f"Loading framework from {FRAMEWORK_PATH}...")
    with FRAMEWORK_PATH.open("r", encoding="utf-8") as f:
        corpus = json.load(f)

    docs = corpus["documents"]
    print(f"Found {len(docs)} documents.")

    print(f"Loading tokenizer and ONNX model from {MODEL_DIR}...")
    tokenizer = Tokenizer.from_file(str(MODEL_DIR / "tokenizer.json"))
    tokenizer.enable_truncation(max_length=128)
    tokenizer.enable_padding(length=128)

    session = ort.InferenceSession(str(MODEL_DIR / "model.onnx"))

    texts_to_embed = []
    metadata = []

    for idx, doc in enumerate(docs):
        # Create rich semantic text representation
        title = doc.get("title", "")
        doc_type = doc.get("type", "skill")
        aliases = ", ".join(doc.get("aliases", []))
        related = ", ".join(doc.get("related_skills", []))
        category = doc.get("category", "")
        description = doc.get("description", "")
        prerequisites = ", ".join(doc.get("prerequisites", []))

        searchable_text = f"{title}. Category: {category}. Aliases: {aliases}. Description: {description}. Related skills: {related}. Prerequisites: {prerequisites}."
        texts_to_embed.append(searchable_text)

        metadata.append({
            "index": idx,
            "id": doc.get("id"),
            "type": doc_type,
            "title": title,
            "category": category,
            "aliases": doc.get("aliases", []),
            "related_skills": doc.get("related_skills", []),
            "prerequisites": doc.get("prerequisites", []),
            "learning_order": doc.get("learning_order", []),
            "description": description
        })

    print(f"Encoding {len(texts_to_embed)} documents into embeddings...")
    # Batch encode
    batch_size = 32
    all_embeddings = []

    for i in range(0, len(texts_to_embed), batch_size):
        batch_texts = texts_to_embed[i:i + batch_size]
        encodings = tokenizer.encode_batch(batch_texts)

        input_ids = np.array([e.ids for e in encodings], dtype=np.int64)
        attention_mask = np.array([e.attention_mask for e in encodings], dtype=np.int64)
        token_type_ids = np.array([e.type_ids for e in encodings], dtype=np.int64)

        outputs = session.run(None, {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "token_type_ids": token_type_ids
        })
        token_embeddings = outputs[0]  # [B, 128, 384]

        # Mean pooling
        mask_expanded = np.expand_dims(attention_mask, -1).astype(float)
        sum_embeddings = np.sum(token_embeddings * mask_expanded, axis=1)
        sum_mask = np.clip(mask_expanded.sum(axis=1), a_min=1e-9, a_max=None)
        batch_pooled = sum_embeddings / sum_mask

        # L2 normalize
        batch_normalized = batch_pooled / np.linalg.norm(batch_pooled, axis=1, keepdims=True)
        all_embeddings.append(batch_normalized)

    matrix = np.vstack(all_embeddings).astype(np.float32)
    print(f"Computed matrix shape: {matrix.shape}")

    np.save(EMBEDDINGS_PATH, matrix)
    with METADATA_PATH.open("w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print(f"Saved embeddings to {EMBEDDINGS_PATH} and metadata to {METADATA_PATH}.")

if __name__ == "__main__":
    compute_embeddings()
