from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import torch
from transformers import AutoModel, AutoTokenizer


@dataclass
class SimilarityResult:
    similarity: float
    evidence: str


class BertSemanticScorer:
    """Interpretable BERT baseline for rubric-to-response semantic matching."""

    def __init__(self, model_name: str = "bert-base-uncased", max_length: int = 512):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.model.eval()
        self.max_length = max_length

    @torch.inference_mode()
    def embed(self, texts: list[str]) -> np.ndarray:
        batch = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=self.max_length,
            return_tensors="pt",
        )
        output = self.model(**batch).last_hidden_state
        mask = batch["attention_mask"].unsqueeze(-1)
        pooled = (output * mask).sum(1) / mask.sum(1).clamp(min=1)
        vectors = pooled.cpu().numpy()
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        return vectors / np.clip(norms, 1e-12, None)

    def similarity(self, a: str, b: str) -> float:
        vectors = self.embed([a, b])
        return float(np.dot(vectors[0], vectors[1]))

    def best_evidence(self, response: str, criterion: str) -> SimilarityResult:
        sentences = [s.strip() for s in response.replace("!", ".").replace("?", ".").split(".") if s.strip()]
        if not sentences:
            return SimilarityResult(0.0, "")

        vectors = self.embed([criterion] + sentences)
        criterion_vec = vectors[0]
        sentence_vecs = vectors[1:]
        scores = sentence_vecs @ criterion_vec
        index = int(np.argmax(scores))
        return SimilarityResult(float(scores[index]), sentences[index])
