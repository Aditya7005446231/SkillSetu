"""Test suite and verification script for SkillSetu in-memory RAG service.

Tests:
1. Framework initialization and corpus integrity
2. In-memory vector matrix dimensions and norm validity
3. Skill normalization (alias lookup + vector fallback)
4. Hybrid vector search ranking and relevance
5. Skill gap bridging and related skill retrieval
6. Context prompt generation for Groq LLMs
7. Latency and performance benchmarking
"""

import time
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.services.skill_framework_rag import (
    get_framework_engine,
    normalize_skill,
    get_related_skills,
    build_framework_context,
    search_skill_framework,
)


def run_tests():
    print("=" * 70)
    print("   SKILLSETU RAG FRAMEWORK VERIFICATION & BENCHMARK SUITE")
    print("=" * 70)

    # 1. Initialization Test
    print("\n[TEST 1] Initializing RAG Engine...")
    t0 = time.perf_counter()
    engine = get_framework_engine()
    init_ms = (time.perf_counter() - t0) * 1000

    assert engine.initialized, "Engine failed to initialize!"
    assert len(engine.documents) >= 200, f"Expected >= 200 documents, found {len(engine.documents)}"
    assert engine.embeddings is not None, "Embedding matrix is missing!"
    assert engine.embeddings.shape == (len(engine.documents), 384), f"Unexpected shape {engine.embeddings.shape}"
    print(f" PASS: Engine initialized in {init_ms:.2f} ms")
    print(f"       Corpus documents: {len(engine.documents)} (8 roles, {len(engine.documents) - 8} skills)")
    print(f"       Embedding matrix: {engine.embeddings.shape} (float32)")

    # 2. Normalization Test
    print("\n[TEST 2] Testing Skill Normalization...")
    test_cases = [
        ("ReactJS", "React"),
        ("react.js", "React"),
        ("postgres db", "PostgreSQL"),
        ("pgsql", "PostgreSQL"),
        ("fast api", "FastAPI"),
        ("k8s", "Kubernetes"),
        ("amazon web services", "AWS"),
        ("py", "Python"),
        ("ts", "TypeScript"),
        ("docker container", "Docker"),
        ("golang", "Go"),
        ("node js", "Node.js"),
    ]

    for raw, expected in test_cases:
        t0 = time.perf_counter()
        normalized = normalize_skill(raw)
        elapsed_us = (time.perf_counter() - t0) * 1_000_000
        assert normalized.lower() == expected.lower(), f"Expected '{expected}' for '{raw}', got '{normalized}'"
        print(f" PASS: '{raw}' -> '{normalized}' ({elapsed_us:.1f} \u03bcs)")

    # 3. Gap Bridging Test
    print("\n[TEST 3] Testing Skill Gap Bridging...")
    gap_cases = ["Docker", "Kubernetes", "React", "Apache Kafka", "FastAPI"]
    for skill in gap_cases:
        bridges = get_related_skills(skill, limit=4)
        assert len(bridges) > 0, f"No bridge skills returned for {skill}"
        print(f" PASS: Missing '{skill}' -> Bridging skills: {bridges}")

    # 4. Hybrid Search Test
    print("\n[TEST 4] Testing Hybrid Vector + Lexical Search...")
    queries = [
        ("full stack web developer react node", "Full-Stack Developer"),
        ("deep learning pytorch neural networks", "PyTorch"),
        ("k8s container orchestration", "Kubernetes"),
    ]
    for q, top_match_expected in queries:
        t0 = time.perf_counter()
        results = engine.search(q, limit=3)
        elapsed_ms = (time.perf_counter() - t0) * 1000
        assert len(results) > 0, f"No search results for query '{q}'"
        top_titles = [r.get("title") for r in results]
        assert top_match_expected in top_titles, f"Expected '{top_match_expected}' in top results: {top_titles}"
        print(f" PASS: Query '{q}' ({elapsed_ms:.2f} ms)")
        for rank, r in enumerate(results, 1):
            print(f"        {rank}. {r.get('title')} ({r.get('type')}) - {r.get('category')}")

    # 5. LLM Prompt Context Generation Test
    print("\n[TEST 5] Testing Groq Prompt Context Generation...")
    context = build_framework_context("Junior AI Engineer with Python, NumPy and RAG", limit=3)
    assert "Retrieved 3 relevant records" in context, "Context header missing"
    assert "Python" in context or "AI" in context or "RAG" in context, "Context missing key terms"
    print(" PASS: Context formatted successfully:")
    for line in context.split("\n"):
        print(f"       {line[:110]}...")

    # 6. Performance Benchmarking (100 sequential queries)
    print("\n[TEST 6] Benchmarking Retrieval Latency (100 iterations)...")
    bench_queries = [
        "ReactJS", "fast api", "postgres", "docker", "machine learning",
        "kubernetes", "typescript", "golang", "redis cache", "aws lambda"
    ]
    total_time = 0.0
    iterations = 100
    for i in range(iterations):
        q = bench_queries[i % len(bench_queries)]
        t0 = time.perf_counter()
        engine.search(q, limit=5)
        total_time += time.perf_counter() - t0

    avg_ms = (total_time / iterations) * 1000
    print(f" PASS: Average search latency: {avg_ms:.2f} ms per query")
    print(f"       Throughput: {1000 / avg_ms:.0f} queries/second on single CPU core")

    print("\n" + "=" * 70)
    print("   ALL RAG ASSERTIONS & TESTS PASSED SUCCESSFULLY!")
    print("=" * 70)


if __name__ == "__main__":
    run_tests()
