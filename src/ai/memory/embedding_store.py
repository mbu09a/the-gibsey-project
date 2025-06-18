from __future__ import annotations
import json, pathlib, uuid
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Iterable
import torch, torch.nn.functional as F
from sentence_transformers import SentenceTransformer

@dataclass
class MemoryEntry:
    id: str
    text: str
    embedding: List[float]
    meta: Dict[str, Any]

    def to_json(self):
        return json.dumps(asdict(self), ensure_ascii=False)

class EmbeddingStore:
    def __init__(self, path: str = "src/ai/memory/memory.jsonl",
                 model_name: str = "all-mpnet-base-v2"):
        self.path = pathlib.Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.model = SentenceTransformer(model_name, device="cpu")
        self.entries: List[MemoryEntry] = []
        if self.path.exists():
            with self.path.open() as f:
                for line in f:
                    obj = json.loads(line)
                    self.entries.append(MemoryEntry(**obj))

    # ─── Public API ────────────────────────────────────────────
    def add(self, text: str, meta: Dict[str, Any]) -> MemoryEntry:
        emb = self._embed(text)
        entry = MemoryEntry(id=str(uuid.uuid4()), text=text,
                            embedding=emb.tolist(), meta=meta)
        self.entries.append(entry)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(entry.to_json() + "\n")
        return entry

    def search(self, query: str | Iterable[str], k: int = 8,
               filters: Dict[str, Any] | None = None) -> List[tuple[MemoryEntry,float]]:
        q_emb = self._embed(query)
        sims = []
        for e in self._filter(filters):
            sim = F.cosine_similarity(
                q_emb.view(1, -1), torch.tensor(e.embedding).view(1, -1)
            ).item()
            sims.append((e, sim))
        return sorted(sims, key=lambda x: x[1], reverse=True)[:k]

    # ─── Internals ─────────────────────────────────────────────
    def _embed(self, txt: str | Iterable[str]):
        if isinstance(txt, str):
            txt = [txt]
        vec = self.model.encode(list(txt), convert_to_tensor=True,
                                device="cpu", normalize_embeddings=True)
        return vec.mean(dim=0)

    def _filter(self, filters):
        if not filters:
            return self.entries
        def keep(e):
            return all(e.meta.get(k) == v for k, v in filters.items())
        return filter(keep, self.entries)