"""Pipeline v3 — configuración PRE-REGISTRADA (SPIKE Fase 1).

Todo lo que la medición necesita cuelga de aquí. Commit a git = pre-registro
(metodología v2, Fase 2). No modificar tras congelar sin re-versionar `INGEST_VERSION`.
"""
import os
import json
from dataclasses import dataclass, asdict
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

# ── Paths ──
PROJECT_ROOT = Path(__file__).parent.parent
POLICIES_DIR = PROJECT_ROOT / "policies"
METADATA_FILE = POLICIES_DIR / "metadata.json"
CHROMA_DIR = PROJECT_ROOT / ".chroma_db"
WEB_DATA_DIR = PROJECT_ROOT / "web" / "data"
CODEBOOK_FILE = Path(__file__).parent / "codebook.json"
CACHE_DIR = Path(__file__).parent / "cache"          # blurbs + salidas crudas cacheadas

# ── Pipeline params (pre-registrados) ──
INGEST_VERSION = "v3.0"
COLLECTION_V3 = "politicas_v3"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"   # multilingüe, local, reproducible
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"        # una API para TODAS las familias
CONTEXT_BLURB_MODEL = "openai/gpt-4o-mini"                  # Anthropic-style contextual retrieval (vía OpenRouter)
CLASSIFIER_TEMPERATURE = 0.0                                 # determinismo
CLASSIFIER_MAX_RETRIES = 3                                   # Fase 5: glm/kimi fallan de forma intermitente
CLASSIFIER_BACKOFF_SEC = 2.0                                 # backoff exponencial entre reintentos
# Fase 5: con 400 tokens, glm-4.6 (modelo de razonamiento) gastaba TODO el presupuesto
# en la cadena de razonamiento y devolvía content=None (finish_reason=length) → 30/70
# fallos. No se suprime el razonamiento: cada familia debe leer el códebook como lo
# haría naturalmente. Se le da techo suficiente.
# (1500 aún truncaba a glm en los 12 pasajes más largos; 4000 le da margen holgado.)
CLASSIFIER_MAX_TOKENS = 4000
K_PASSAGES = 10             # pasajes de gobernanza por país (Fase 4 usó 3; Fase 5 sube a 10)
TRANSLATION_MODEL = "openai/gpt-4o-mini"                     # ZH/ES/DE → EN para el panel (Vía B)

# ── Esquema de metadata (dos capas) ──
# Tier A: manual/determinista, nivel documento. `genre` = control del confusor (NUNCA por LLM).
TIER_A_FIELDS = {
    "doc_id": str, "country": str, "region": str,
    "genre": str, "language": str, "year": int,
    "adopting_body": str, "doc_type_official": str,
    "source_uri": str, "n_pages": int, "ingest_version": str,
}
GENRE_VOCAB = ["strategy", "law", "action_plan", "report", "guidance"]   # vocabulario controlado (spike Fase 2b: +guidance)
# Campos indexados/filtrables (bajos en cardinalidad — guía Pinecone):
FILTERABLE_FIELDS = ["country", "region", "genre", "language", "year"]

# Tier B: auto, congelado-cacheado, SOLO retrieval.
TIER_B_FIELDS = {
    "chunk_id": str, "parent_doc_id": str, "chunk_index": int,
    "page": int, "char_start": int, "char_end": int,
    "context": str, "emb_model": str, "ctx_model": str,
}

# ── Panel de jueces (etiquetado por ORIGEN para el contraste transcultural) ──
@dataclass
class Judge:
    key: str
    provider: str        # openai | google | together | anthropic
    model: str
    origin: str          # "western" | "chinese"
    env_key: str         # variable de entorno con la API key

# Panel PUNTUADO (7 jueces vía OpenRouter, etiquetados por origen). Claude NO va aquí.
PANEL = [
    Judge("gpt",      "openrouter", "openai/gpt-4o-mini",                 "western", "OPENROUTER_API_KEY"),
    Judge("gemini",   "openrouter", "google/gemini-2.5-flash",           "western", "OPENROUTER_API_KEY"),
    Judge("llama",    "openrouter", "meta-llama/llama-3.3-70b-instruct", "western", "OPENROUTER_API_KEY"),
    # Fase 5: `qwen/qwen-2.5-72b-instruct` fue RETIRADO de OpenRouter (de ahí el error de
    # ruteo de la Fase 2-pre; no era el provider). Reemplazo fijado por fecha (2507) para
    # reproducibilidad. Re-versionado documentado en el spike-log — el pre-registro no se
    # rompe en silencio.
    Judge("qwen",     "openrouter", "qwen/qwen3-235b-a22b-2507",         "chinese", "OPENROUTER_API_KEY"),
    Judge("deepseek", "openrouter", "deepseek/deepseek-chat",            "chinese", "OPENROUTER_API_KEY"),
    Judge("glm",      "openrouter", "z-ai/glm-4.6",                      "chinese", "OPENROUTER_API_KEY"),
    Judge("kimi",     "openrouter", "moonshotai/kimi-k2",                "chinese", "OPENROUTER_API_KEY"),
]

# META-JUEZ: adjudica SOLO los desacuerdos del panel + sintetiza. NO puntúa
# (evita circularidad: Claude orquestó el pipeline y coordinó el códebook).
META_JUDGE = Judge("claude", "openrouter", "anthropic/claude-sonnet-4.5", "western", "OPENROUTER_API_KEY")

def available_judges():
    """Jueces con API key presente en el entorno."""
    return [j for j in PANEL if os.getenv(j.env_key)]

def load_codebook() -> dict:
    return json.loads(CODEBOOK_FILE.read_text(encoding="utf-8"))

# ── Ejes confucianos (Vía A = embeddings; Vía B = LLM para dézhì) ──
# Se reutilizan los 6 ejes tuned validados en pipeline/config.py (A/B ganador: híbrido+tuned6).
AXES = ["ren", "li", "yi", "xiushen", "dezhi_fa", "he"]
AXIS_LLM = "dezhi_fa"   # el eje difícil que va por Vía B (clasificador)


if __name__ == "__main__":
    print(f"INGEST_VERSION={INGEST_VERSION}  collection={COLLECTION_V3}")
    print(f"chunk={CHUNK_SIZE}/{CHUNK_OVERLAP}  emb={EMBEDDING_MODEL}")
    print(f"Tier A: {len(TIER_A_FIELDS)} campos  |  Tier B: {len(TIER_B_FIELDS)} campos")
    print(f"genre vocab: {GENRE_VOCAB}")
    av = available_judges()
    print(f"Panel: {len(PANEL)} jueces definidos, {len(av)} disponibles con keys:")
    for j in PANEL:
        ok = "✓" if os.getenv(j.env_key) else "—"
        print(f"  [{ok}] {j.key:9s} {j.origin:8s} {j.model}")
    cb = load_codebook()
    print(f"Códebook '{cb['axis']}': {len(cb['decision_rules'])} reglas, "
          f"{len(cb['examples_positive'])}+/{len(cb['examples_negative'])}- ejemplos")
