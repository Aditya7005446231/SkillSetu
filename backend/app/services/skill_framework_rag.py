"""In-memory RAG service over SkillSetu skill framework.

Uses all-MiniLM-L6-v2 ONNX embeddings kept in memory via NumPy,
hybrid lexical/semantic scoring, canonical skill normalization, and
gap-bridging related skill retrieval.
"""

from functools import lru_cache
import json
import logging
from pathlib import Path
import re
from typing import Any

import numpy as np

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
FRAMEWORK_PATH = DATA_DIR / "skill_framework.json"
MODEL_DIR = DATA_DIR / "models" / "all-MiniLM-L6-v2"
EMBEDDINGS_PATH = DATA_DIR / "skill_embeddings.npy"
METADATA_PATH = DATA_DIR / "skill_metadata.json"


def _clean_text(value: str) -> str:
    """Normalize text for lexical comparison."""
    cleaned = re.sub(r"[^a-z0-9+#]+", " ", (value or "").lower())
    return re.sub(r"\s+", " ", cleaned).strip()


class SkillFrameworkEngine:
    """In-memory vector & lexical engine for the SkillSetu taxonomy."""

    def __init__(self):
        self.initialized = False
        self.documents: list[dict[str, Any]] = []
        self.metadata: list[dict[str, Any]] = []
        self.embeddings: np.ndarray | None = None
        self.tokenizer = None
        self.onnx_session = None
        self.alias_to_canonical: dict[str, str] = {}
        self.name_to_doc: dict[str, dict[str, Any]] = {}
        self.framework_version: str = "v2"
        self._load()

    def _load(self):
        try:
            # 1. Load framework JSON
            if not FRAMEWORK_PATH.exists():
                logger.error("Framework file not found: %s", FRAMEWORK_PATH)
                return

            with FRAMEWORK_PATH.open("r", encoding="utf-8") as f:
                corpus = json.load(f)
            self.documents = corpus.get("documents", [])
            self.framework_version = corpus.get("framework_version", "v2")

            # 2. Build fast lookup dictionaries
            for doc in self.documents:
                title = doc.get("title") or doc.get("name", "")
                title_clean = _clean_text(title)
                self.name_to_doc[title_clean] = doc
                self.alias_to_canonical[title_clean] = title

                for alias in doc.get("aliases", []):
                    alias_clean = _clean_text(alias)
                    if alias_clean:
                        self.alias_to_canonical[alias_clean] = title

            # 3. Load precomputed embeddings and metadata if available
            if EMBEDDINGS_PATH.exists() and METADATA_PATH.exists():
                self.embeddings = np.load(EMBEDDINGS_PATH)
                with METADATA_PATH.open("r", encoding="utf-8") as f:
                    self.metadata = json.load(f)
                logger.info(
                    "Loaded in-memory skill embeddings: shape %s",
                    self.embeddings.shape,
                )
            else:
                logger.warning("Skill embeddings not precomputed on disk.")

            # 4. Load ONNX model and tokenizer for on-the-fly query encoding
            if (MODEL_DIR / "model.onnx").exists() and (MODEL_DIR / "tokenizer.json").exists():
                try:
                    import onnxruntime as ort
                    from tokenizers import Tokenizer

                    self.tokenizer = Tokenizer.from_file(str(MODEL_DIR / "tokenizer.json"))
                    self.tokenizer.enable_truncation(max_length=128)
                    self.tokenizer.enable_padding(length=128)

                    # Optimize ONNX session for CPU inference
                    opts = ort.SessionOptions()
                    opts.intra_op_num_threads = 2
                    opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
                    self.onnx_session = ort.InferenceSession(
                        str(MODEL_DIR / "model.onnx"),
                        sess_options=opts,
                        providers=["CPUExecutionProvider"],
                    )
                    logger.info("ONNX all-MiniLM-L6-v2 inference session ready.")
                except Exception as e:
                    logger.warning("Failed to initialize ONNX session: %s", e)

            self.initialized = True
        except Exception as e:
            logger.exception("Error initializing SkillFrameworkEngine: %s", e)

    def encode(self, text: str) -> np.ndarray | None:
        """Encode a single text into a 384-d normalized vector using ONNX."""
        if not self.onnx_session or not self.tokenizer:
            return None

        try:
            enc = self.tokenizer.encode(text)
            inputs = {
                "input_ids": np.array([enc.ids], dtype=np.int64),
                "attention_mask": np.array([enc.attention_mask], dtype=np.int64),
                "token_type_ids": np.array([enc.type_ids], dtype=np.int64),
            }
            outputs = self.onnx_session.run(None, inputs)
            token_embeddings = outputs[0]  # [1, 128, 384]

            # Mean pooling over attention mask
            mask = np.expand_dims(inputs["attention_mask"], -1).astype(float)
            pooled = np.sum(token_embeddings * mask, axis=1) / np.clip(
                mask.sum(axis=1), 1e-9, None
            )
            normalized = pooled / np.linalg.norm(pooled, axis=1, keepdims=True)
            return normalized[0].astype(np.float32)
        except Exception as e:
            logger.warning("Encoding failed for text '%s': %s", text[:50], e)
            return None

    def search(
        self,
        query: str,
        limit: int = 5,
        filter_type: str | None = None,
    ) -> list[dict[str, Any]]:
        """Hybrid search combining dense vector cosine similarity and exact alias matching."""
        if not self.documents:
            return []

        cleaned_query = _clean_text(query)
        query_terms = set(cleaned_query.split())

        # Vector scores (if available)
        query_vec = self.encode(query)
        vector_scores = np.zeros(len(self.documents), dtype=np.float32)

        if query_vec is not None and self.embeddings is not None and len(self.embeddings) == len(self.documents):
            # Cosine similarity via NumPy dot product
            vector_scores = np.dot(self.embeddings, query_vec)

        results = []
        for idx, doc in enumerate(self.documents):
            doc_type = doc.get("type", "skill")
            if filter_type and doc_type != filter_type:
                continue

            title = doc.get("title") or doc.get("name", "")
            title_clean = _clean_text(title)
            aliases = [_clean_text(a) for a in doc.get("aliases", [])]

            # Lexical exact and partial boosts
            lexical_boost = 0.0
            if cleaned_query == title_clean:
                lexical_boost += 1.5  # Exact title match
            elif cleaned_query in aliases:
                lexical_boost += 1.4  # Exact alias match
            elif any(alias == cleaned_query for alias in aliases):
                lexical_boost += 1.2
            else:
                # Token overlap
                doc_terms = set(title_clean.split())
                for alias in aliases:
                    doc_terms.update(alias.split())
                overlap = len(query_terms & doc_terms)
                if overlap > 0:
                    lexical_boost += 0.25 * overlap

            v_score = float(vector_scores[idx]) if idx < len(vector_scores) else 0.0
            total_score = v_score + lexical_boost

            if total_score > 0.25 or lexical_boost > 0:
                results.append(
                    {
                        "document": doc,
                        "score": round(float(total_score), 4),
                        "vector_similarity": round(float(v_score), 4),
                        "lexical_boost": round(float(lexical_boost), 4),
                    }
                )

        results.sort(key=lambda r: r["score"], reverse=True)
        return [r["document"] for r in results[:limit]]

    def normalize_skill(
        self,
        raw_skill: str,
        threshold: float = 0.58,
    ) -> str:
        """Canonicalize skill strings (e.g. 'ReactJS' -> 'React', 'postgres db' -> 'PostgreSQL')."""
        if not raw_skill or not raw_skill.strip():
            return raw_skill

        cleaned = _clean_text(raw_skill)

        # 1. Direct fast lookup in aliases or exact title
        if cleaned in self.alias_to_canonical:
            return self.alias_to_canonical[cleaned]

        # 2. In-memory vector match via all-MiniLM-L6-v2
        query_vec = self.encode(raw_skill)
        if query_vec is not None and self.embeddings is not None:
            sims = np.dot(self.embeddings, query_vec)
            best_idx = int(np.argmax(sims))
            best_score = float(sims[best_idx])

            if best_score >= threshold:
                best_doc = self.documents[best_idx]
                if best_doc.get("type") == "skill":
                    return best_doc.get("title") or best_doc.get("name")

        # Fallback: capitalize clean words
        return raw_skill.strip()

    def get_related_skills_for_gap(
        self,
        missing_skill: str,
        limit: int = 4,
    ) -> list[str]:
        """Fetch related skills to bridge a missing skill gap."""
        try:
            limit_val = int(limit)
        except (ValueError, TypeError):
            limit_val = 4
        canonical_name = self.normalize_skill(missing_skill)
        doc = self.name_to_doc.get(_clean_text(canonical_name))

        if not doc:
            # Use vector search to find closest skill
            matches = self.search(missing_skill, limit=1, filter_type="skill")
            if matches:
                doc = matches[0]

        if not doc:
            return []

        related = list(doc.get("related_skills", []))
        prereqs = list(doc.get("prerequisites", []))

        # Combine prerequisites and related skills
        combined = []
        for s in prereqs + related:
            if s and s not in combined and s.lower() != canonical_name.lower():
                combined.append(s)

        return combined[:limit_val]


# Singleton engine instance
_engine: SkillFrameworkEngine | None = None


def get_framework_engine() -> SkillFrameworkEngine:
    global _engine
    if _engine is None:
        _engine = SkillFrameworkEngine()
    return _engine


def retrieve_framework_context(query: str, limit: int = 5) -> list[dict]:
    """Retrieve top framework documents for a query."""
    return get_framework_engine().search(query, limit=limit)


def normalize_skill(value: str) -> str:
    """Normalize a skill using alias table and all-MiniLM-L6-v2 vector embeddings."""
    return get_framework_engine().normalize_skill(value)


def get_related_skills(missing_skill: str, limit: int = 4) -> list[str]:
    """Fetch related skills and prerequisites for a missing skill gap."""
    return get_framework_engine().get_related_skills_for_gap(missing_skill, limit=limit)


def build_framework_context(query: str, limit: int = 6) -> str:
    """Format retrieved framework documents for Groq LLM prompts."""
    engine = get_framework_engine()
    documents = engine.search(query, limit=limit)

    if not documents:
        return "No matching skill-framework records were retrieved."

    lines = [
        f"Retrieved {len(documents)} relevant records from {engine.framework_version}:"
    ]
    for doc in documents:
        doc_type = doc.get("type", "skill")
        title = doc.get("title") or doc.get("name", "")
        desc = doc.get("description", "")
        aliases = ", ".join(doc.get("aliases", []))
        related = ", ".join(doc.get("related_skills", []))
        prereqs = ", ".join(doc.get("prerequisites", []))
        learning_order = ", ".join(doc.get("learning_order", []))

        line = f"- {title} ({doc_type}): {desc}"
        if aliases:
            line += f" | Aliases: {aliases}."
        if related:
            line += f" | Related skills: {related}."
        if prereqs:
            line += f" | Prerequisites: {prereqs}."
        if learning_order:
            line += f" | Recommended learning order: {learning_order}."
        lines.append(line)

    return "\n".join(lines)


def search_skill_framework(query: str, limit: int = 10) -> dict:
    """Public search function for API endpoint."""
    engine = get_framework_engine()
    docs = engine.search(query, limit=limit)
    return {
        "framework_version": engine.framework_version,
        "query": query,
        "count": len(docs),
        "documents": docs,
    }
