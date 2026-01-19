from __future__ import annotations

import hashlib
import math
import os
from dataclasses import dataclass
from typing import List, Optional, Protocol


class EmbeddingAdapter(Protocol):
    dim: int

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        ...


@dataclass
class MockHashEmbedding:
    """Deterministic local embedding.

    - No external API.
    - Suitable for pipeline wiring and regression harness.
    - Not suitable for semantic quality evaluation.
    """

    dim: int = 128

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        out: List[List[float]] = []
        for t in texts:
            # Stable hash -> pseudo-random bytes
            h = hashlib.sha256((t or "").encode("utf-8")).digest()
            # Expand to dim
            vec: List[float] = []
            i = 0
            while len(vec) < self.dim:
                b = h[i % len(h)]
                vec.append(b / 255.0)
                i += 1
            # L2 normalize
            norm = math.sqrt(sum(x * x for x in vec)) or 1.0
            vec = [x / norm for x in vec]
            out.append(vec)
        return out


def build_embedding_adapter(cfg: dict) -> EmbeddingAdapter:
    provider = (cfg.get("provider") or "mock").lower()
    if provider == "mock":
        dim = int(cfg.get("dim") or 128)
        return MockHashEmbedding(dim=dim)

    if provider == "openai":
        # Optional dependency: openai
        try:
            from openai import OpenAI
        except Exception as e:  # pragma: no cover
            raise RuntimeError("openai python package is not installed. Use provider=mock or install openai.") from e

        model = cfg.get("model") or "text-embedding-3-small"
        client = OpenAI()

        class _OpenAIEmbedding:
            dim = 0

            def embed_texts(self, texts: List[str]) -> List[List[float]]:
                res = client.embeddings.create(model=model, input=texts)
                return [d.embedding for d in res.data]

            def embed_documents(self, texts: List[str]) -> List[List[float]]:
                return self.embed_texts(texts)

            def embed_query(self, text: str) -> List[float]:
                return self.embed_texts([text])[0]

        return _OpenAIEmbedding()

    if provider == "google":
        # Google Generative AI (google-genai) embedding adapter
        try:
            from google import genai
            from google.genai import types
        except Exception as e:  # pragma: no cover
            raise RuntimeError(
                "google-genai python package is not installed. "
                "Use provider=mock or install google-genai."
            ) from e

        api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GOOGLE_API_KEY 또는 GEMINI_API_KEY 환경변수가 필요합니다. "
                ".env 파일에 설정하거나 환경변수로 지정해주세요."
            )

        model = cfg.get("model") or "gemini-embedding-001"
        output_dimensionality: Optional[int] = cfg.get("output_dimensionality")

        client = genai.Client(api_key=api_key)

        class _GoogleEmbedding:
            dim = output_dimensionality or 768  # gemini-embedding-001 default

            def _parse_embeddings(self, result) -> List[List[float]]:
                """Parse embeddings from response, robust to response format changes."""
                embeddings = result.embeddings
                parsed: List[List[float]] = []
                for emb in embeddings:
                    if hasattr(emb, "values"):
                        parsed.append(list(emb.values))
                    else:
                        parsed.append(list(emb))
                return parsed

            def embed_documents(self, texts: List[str]) -> List[List[float]]:
                config_kwargs = {"task_type": "RETRIEVAL_DOCUMENT"}
                if output_dimensionality:
                    config_kwargs["output_dimensionality"] = output_dimensionality
                config = types.EmbedContentConfig(**config_kwargs)
                result = client.models.embed_content(
                    model=model,
                    contents=texts,
                    config=config,
                )
                return self._parse_embeddings(result)

            def embed_query(self, text: str) -> List[float]:
                config_kwargs = {"task_type": "RETRIEVAL_QUERY"}
                if output_dimensionality:
                    config_kwargs["output_dimensionality"] = output_dimensionality
                config = types.EmbedContentConfig(**config_kwargs)
                result = client.models.embed_content(
                    model=model,
                    contents=text,
                    config=config,
                )
                parsed = self._parse_embeddings(result)
                return parsed[0] if parsed else []

            def embed_texts(self, texts: List[str]) -> List[List[float]]:
                """Protocol compatibility: internally calls embed_documents."""
                return self.embed_documents(texts)

        return _GoogleEmbedding()

    raise ValueError(f"Unsupported embedding provider: {provider}")
