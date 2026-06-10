"""Configuración del pipeline de análisis."""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ── Paths ──
PROJECT_ROOT = Path(__file__).parent.parent
POLICIES_DIR = PROJECT_ROOT / "policies"
RAW_DIR = POLICIES_DIR / "raw"
PROCESSED_DIR = POLICIES_DIR / "processed"
METADATA_FILE = POLICIES_DIR / "metadata.json"
WEB_DATA_DIR = PROJECT_ROOT / "web" / "data"
FIGURES_DIR = PROJECT_ROOT / "document" / "figures" / "generated"
CHROMA_DIR = PROJECT_ROOT / ".chroma_db"

# ── Embeddings ──
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
USE_LOCAL_EMBEDDINGS = os.getenv("USE_LOCAL_EMBEDDINGS", "0") == "1"
EMBEDDING_MODEL_OPENAI = "text-embedding-3-small"
EMBEDDING_MODEL_LOCAL = "paraphrase-multilingual-MiniLM-L12-v2"

# ── Chunking ──
CHUNK_SIZE = 800
CHUNK_OVERLAP = 200

# ── ChromaDB ──
COLLECTION_NAME = "politicas_ia_educacion"

# ── Chroma Cloud (redundancy) ──
CHROMA_CLOUD_API_KEY = os.getenv("CHROMA_CLOUD_API_KEY", "")
CHROMA_CLOUD_TENANT = os.getenv("CHROMA_CLOUD_TENANT", "")
CHROMA_CLOUD_DATABASE = os.getenv("CHROMA_CLOUD_DATABASE", "public-policy")

# ── Analysis dimensions ──
DIMENSIONS = {
    "gobernanza": {
        "label": "Gobernanza y regulación",
        "query": "Regulación gubernamental, marcos legales, gobernanza de inteligencia artificial en educación, leyes, normativas, supervisión estatal, políticas de implementación",
    },
    "curriculo": {
        "label": "Currículo e integración educativa",
        "query": "Currículo escolar, integración de inteligencia artificial en planes de estudio, competencias digitales, contenidos educativos, alfabetización en IA, programas académicos",
    },
    "formacion_docente": {
        "label": "Formación docente",
        "query": "Formación de profesores en inteligencia artificial, capacitación docente, desarrollo profesional, competencias pedagógicas digitales, preparación del profesorado",
    },
    "infraestructura": {
        "label": "Infraestructura y acceso",
        "query": "Infraestructura tecnológica educativa, acceso a internet, equipamiento escolar, conectividad, recursos digitales, inversión en tecnología educativa",
    },
    "etica": {
        "label": "Ética y valores",
        "query": "Ética de la inteligencia artificial en educación, privacidad de datos estudiantiles, sesgo algorítmico, transparencia, responsabilidad, valores humanos",
    },
    "investigacion": {
        "label": "Investigación e innovación",
        "query": "Investigación en inteligencia artificial educativa, innovación pedagógica, desarrollo de tecnología educativa, centros de investigación, financiamiento de I+D",
    },
    "equidad": {
        "label": "Equidad e inclusión",
        "query": "Equidad educativa, inclusión digital, brecha digital, acceso igualitario a IA en educación, diversidad, poblaciones vulnerables, género en tecnología",
    },
}

# ── Countries & regions ──
# Corpus v3: Sudeste Asiático con clasificación de herencia confuciana (CHC).
# China se incluye como caso ancla de la civilización confuciana (Asia Oriental).
# chc: "fuerte" | "parcial" | "ausente" | "na" (organismos)
COUNTRIES = {
    "china": {"name": "China", "region": "asia_oriental", "chc": "fuerte"},
    "vietnam": {"name": "Vietnam", "region": "sudeste_asiatico", "chc": "fuerte"},
    "singapur": {"name": "Singapur", "region": "sudeste_asiatico", "chc": "fuerte"},
    "malasia": {"name": "Malasia", "region": "sudeste_asiatico", "chc": "parcial"},
    "indonesia": {"name": "Indonesia", "region": "sudeste_asiatico", "chc": "ausente"},
    "tailandia": {"name": "Tailandia", "region": "sudeste_asiatico", "chc": "ausente"},
    "filipinas": {"name": "Filipinas", "region": "sudeste_asiatico", "chc": "ausente"},
    "asean": {"name": "ASEAN", "region": "regional", "chc": "na"},
    "unesco": {"name": "UNESCO", "region": "internacional", "chc": "na"},
}

REGION_COLORS = {
    "asia_oriental": "#880e4f",
    "sudeste_asiatico": "#d32f2f",
    "regional": "#f57c00",
    "internacional": "#7b1fa2",
}

CHC_COLORS = {
    "fuerte": "#b71c1c",
    "parcial": "#f57c00",
    "ausente": "#1976d2",
    "na": "#7b1fa2",
}
