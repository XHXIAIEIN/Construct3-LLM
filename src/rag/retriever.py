"""
Hybrid Retriever for Construct 3 RAG
Combines vector search with optional BM25 for better results
"""
import time
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    from qdrant_client import QdrantClient
except ImportError:
    print("Warning: qdrant-client not installed")


@dataclass
class SearchResult:
    """Represents a search result"""
    text: str
    score: float
    source: str  # collection name
    metadata: Dict[str, Any]


class HybridRetriever:
    """
    Hybrid retriever combining:
    - Vector search (semantic similarity)
    - Optional keyword matching for terms
    """

    def __init__(
        self,
        qdrant_host: str = "localhost",
        qdrant_port: int = 6333,
        embedding_model_name: str = "BAAI/bge-m3"
    ):
        self.client = QdrantClient(host=qdrant_host, port=qdrant_port)
        self.embedding_model_name = embedding_model_name
        self._embedder = None

    @property
    def embedder(self):
        if self._embedder is None:
            logger.info(f"[加载] Embedding 模型: {self.embedding_model_name} ...")
            t0 = time.time()
            from src.data_processing.indexer import EmbeddingModel
            self._embedder = EmbeddingModel(self.embedding_model_name)
            logger.info(f"[加载] Embedding 模型完成 ({time.time()-t0:.1f}s)")
        return self._embedder

    def search_collection(
        self,
        collection_name: str,
        query: str,
        top_k: int = 5,
        score_threshold: float = 0.5
    ) -> List[SearchResult]:
        """Search a single collection"""
        query_vector = self.embedder.encode_single(query)

        try:
            results = self.client.search(
                collection_name=collection_name,
                query_vector=query_vector,
                limit=top_k,
                score_threshold=score_threshold
            )
        except Exception as e:
            print(f"Search error in {collection_name}: {e}")
            return []

        return [
            SearchResult(
                text=r.payload.get("text", ""),
                score=r.score,
                source=collection_name,
                metadata={k: v for k, v in r.payload.items() if k != "text"}
            )
            for r in results
        ]

    def search_manual(self, query: str, top_k: int = 5) -> List[SearchResult]:
        """Search manual documentation"""
        from src.config import COLLECTION_MANUAL
        return self.search_collection(COLLECTION_MANUAL, query, top_k)

    def search_terms(self, query: str, top_k: int = 10) -> List[SearchResult]:
        """Search translation terms"""
        from src.config import COLLECTION_TERMS
        return self.search_collection(COLLECTION_TERMS, query, top_k, score_threshold=0.3)

    def search_examples(self, query: str, top_k: int = 5) -> List[SearchResult]:
        """Search example projects"""
        from src.config import COLLECTION_EXAMPLES
        return self.search_collection(COLLECTION_EXAMPLES, query, top_k)

    def search_all(
        self,
        query: str,
        top_k_per_collection: int = 3
    ) -> Dict[str, List[SearchResult]]:
        """Search all collections and return organized results"""
        results = {
            "manual": self.search_manual(query, top_k_per_collection),
            "terms": self.search_terms(query, top_k_per_collection),
            "examples": self.search_examples(query, top_k_per_collection)
        }
        return results

    def format_context(self, results: Dict[str, List[SearchResult]]) -> str:
        """Format search results as context for LLM"""
        context_parts = []

        # Manual results
        if results.get("manual"):
            context_parts.append("### 手册文档\n")
            for r in results["manual"]:
                source = r.metadata.get("source", "unknown")
                page = r.metadata.get("page", "")
                context_parts.append(f"[来源: {source} P{page}]\n{r.text}\n")

        # Term results
        if results.get("terms"):
            context_parts.append("\n### 术语表\n")
            for r in results["terms"]:
                zh = r.metadata.get("zh", "")
                en = r.metadata.get("en", "")
                context_parts.append(f"- {zh} = {en}")

        # Example results
        if results.get("examples"):
            context_parts.append("\n### 示例代码\n")
            for r in results["examples"]:
                project = r.metadata.get("project", "unknown")
                context_parts.append(f"[项目: {project}]\n{r.text}\n")

        return "\n".join(context_parts)


class TermMatcher:
    """
    Exact term matching for translation assistance
    Uses in-memory term dictionary for fast lookups
    """

    def __init__(self):
        self.terms: Dict[str, Dict[str, str]] = {}  # zh -> {en, key}
        self.terms_en: Dict[str, Dict[str, str]] = {}  # en -> {zh, key}
        self._loaded = False

    def load_terms(self, csv_path: str):
        """Load terms from CSV file"""
        from src.data_processing.csv_parser import CSVParser

        parser = CSVParser()
        entries = parser.parse_file(csv_path)

        for entry in entries:
            self.terms[entry.zh] = {"en": entry.en, "key": entry.term_key}
            self.terms_en[entry.en.lower()] = {"zh": entry.zh, "key": entry.term_key}

        self._loaded = True
        print(f"Loaded {len(self.terms)} terms for matching")

    def match_zh(self, text: str) -> List[Dict[str, str]]:
        """Find exact Chinese term matches in text"""
        matches = []
        for zh, data in self.terms.items():
            if zh in text:
                matches.append({
                    "zh": zh,
                    "en": data["en"],
                    "key": data["key"]
                })
        return matches

    def match_en(self, text: str) -> List[Dict[str, str]]:
        """Find exact English term matches in text"""
        matches = []
        text_lower = text.lower()
        for en, data in self.terms_en.items():
            if en in text_lower:
                matches.append({
                    "zh": data["zh"],
                    "en": en,
                    "key": data["key"]
                })
        return matches

    def translate(self, term: str, to_lang: str = "zh") -> Optional[str]:
        """Translate a single term"""
        if to_lang == "zh":
            data = self.terms_en.get(term.lower())
            return data["zh"] if data else None
        else:
            data = self.terms.get(term)
            return data["en"] if data else None
