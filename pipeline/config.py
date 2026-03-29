"""Configuración del pipeline de análisis — v2.

Reestructurado: 7 países (1 por continente político), China con 7 docs
longitudinales, dimensiones pre-registradas desde literatura.
"""
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
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY", "")
USE_LOCAL_EMBEDDINGS = os.getenv("USE_LOCAL_EMBEDDINGS", "1") == "1"
EMBEDDING_MODEL_OPENAI = "text-embedding-3-small"
EMBEDDING_MODEL_LOCAL = "paraphrase-multilingual-MiniLM-L12-v2"

# ── Translation (for language control analysis) ──
TRANSLATION_MODEL = "Qwen/Qwen2.5-72B-Instruct"
TRANSLATION_FALLBACK = "deepseek-ai/DeepSeek-V3"
TRANSLATION_TEMPERATURE = 0.3

# ── Chunking ──
CHUNK_SIZE = 800
CHUNK_OVERLAP = 200

# ── ChromaDB ──
COLLECTION_NAME = "politicas_ia_educacion_v2"
BIBLIOGRAPHY_COLLECTION_NAME = "bibliografia_referencias"

# ── References (bibliography PDFs for fact-checking) ──
REFERENCES_DIR = PROJECT_ROOT / "references"

# ── Chroma Cloud (redundancy) ──
CHROMA_CLOUD_API_KEY = os.getenv("CHROMA_CLOUD_API_KEY", "")
CHROMA_CLOUD_TENANT = os.getenv("CHROMA_CLOUD_TENANT", "")
CHROMA_CLOUD_DATABASE = os.getenv("CHROMA_CLOUD_DATABASE", "public-policy-v2")

# ── Countries & regions (v2: 7 countries, 1 per political continent) ──
COUNTRIES = {
    # North America
    "eeuu": {
        "name": "Estados Unidos",
        "region": "norteamerica",
        "language": "en",
    },
    "canada": {
        "name": "Canadá",
        "region": "norteamerica",
        "language": "en",
    },
    # Latin America
    "colombia": {
        "name": "Colombia",
        "region": "latinoamerica",
        "language": "es",
    },
    # Europe
    "alemania": {
        "name": "Alemania",
        "region": "europa",
        "language": "de",
    },
    # Africa
    "sudafrica": {
        "name": "Sudáfrica",
        "region": "africa",
        "language": "en",
    },
    # Oceania
    "australia": {
        "name": "Australia",
        "region": "oceania",
        "language": "en",
    },
    # Asia (7 longitudinal documents)
    "china": {
        "name": "China",
        "region": "asia",
        "language": "zh",
        "composite": True,
    },
}

# ── Chinese policy documents (longitudinal 2017-2025) ──
CHINA_DOCUMENTS = {
    "china_ngaidp_2017": {
        "title": "New Generation AI Development Plan",
        "year": 2017,
        "source": "State Council",
        "file": "3_new_gen_ai_development_plan_2017_en.txt",
    },
    "china_ai_innovation_2018": {
        "title": "AI Innovation Action Plan for Higher Education",
        "year": 2018,
        "source": "Ministry of Education",
        "file": "1_ai_innovation_action_plan_2018_en.txt",
    },
    "china_genai_measures_2023": {
        "title": "Interim Measures for Generative AI Services",
        "year": 2023,
        "source": "Cyberspace Administration of China",
        "file": "2_generative_ai_interim_measures_2023_en.txt",
    },
    "china_k12_guidance_2024": {
        "title": "K-12 AI Education Guidance",
        "year": 2024,
        "source": "Ministry of Education",
        "file": "4_k12_ai_education_guidance_2024_en.txt",
    },
    "china_base_schools_2024": {
        "title": "184 AI Education Base Schools",
        "year": 2024,
        "source": "Ministry of Education",
        "file": "5_184_ai_education_base_schools_2024_en.txt",
    },
    "china_digitalization_2025": {
        "title": "Accelerating Education Digitalization",
        "year": 2025,
        "source": "Ministry of Education + 9 departments",
        "file": "6_accelerating_education_digitalization_2025_en.txt",
    },
    "china_smart_education_2025": {
        "title": "Smart Education Strategy 2.0",
        "year": 2025,
        "source": "Ministry of Education",
        "file": "7_smart_education_strategy_2025_en.txt",
    },
}

# ── Composite groups (for aggregated cross-national comparison) ──
COMPOSITE_GROUPS = {
    "china": list(CHINA_DOCUMENTS.keys()),
}

REGION_COLORS = {
    "norteamerica": "#1565c0",
    "latinoamerica": "#388e3c",
    "europa": "#6a1b9a",
    "africa": "#e65100",
    "oceania": "#00838f",
    "asia": "#d32f2f",
}

# ── Analysis dimensions (PRE-REGISTERED) ──
# These dimensions are derived EXCLUSIVELY from the literature review,
# NOT from reading the corpus. They are committed to git BEFORE running
# any analysis. The git history serves as the pre-registration record.
#
# Sources:
#   - UNESCO Beijing Consensus (2019): Areas 1, 2, 5
#   - Miao et al. (2021): curriculum, infrastructure
#   - OECD Digital Education Outlook (2021): research/innovation
#   - Fatima et al. (2020): governance categories
#   - Long & Magerko (2020): AI literacy framework
#   - Ng et al. (2021): 4 dimensions of AI literacy
#
# IMPORTANT: Do NOT modify these queries after ingesting documents.
# Any post-hoc refinement breaks the pre-registration and reintroduces
# the circular validation problem from v1.

DIMENSIONS = {
    "gobernanza": {
        "label": "Gobernanza y regulación",
        "query": (
            "Institutional governance, regulation of artificial intelligence, "
            "legal framework, ministerial coordination, responsible bodies, "
            "centralization versus decentralization of AI policy decisions"
        ),
        "source": "UNESCO Beijing Consensus Area 1; Fatima et al. (2020)",
    },
    "curriculo": {
        "label": "Currículo e integración educativa",
        "query": (
            "School curriculum, integration of AI into subjects, digital "
            "competencies, curricular content, educational levels, AI as "
            "subject of study versus AI as pedagogical tool"
        ),
        "source": "Miao et al. (2021); Long & Magerko (2020)",
    },
    "formacion_docente": {
        "label": "Formación docente",
        "query": (
            "Teacher training in artificial intelligence, professional "
            "development, certification, digital pedagogical competencies, "
            "partnerships with universities and technology companies"
        ),
        "source": "UNESCO Beijing Consensus Area 2",
    },
    "infraestructura": {
        "label": "Infraestructura y acceso",
        "query": (
            "Technological infrastructure, connectivity, school equipment, "
            "digital platforms, internet access, investment in educational "
            "technology, hardware and software provision"
        ),
        "source": "Miao et al. (2021)",
    },
    "etica": {
        "label": "Ética y valores",
        "query": (
            "Ethics of artificial intelligence in education, student data "
            "privacy, algorithmic bias, transparency, human oversight, "
            "academic integrity, responsible AI use"
        ),
        "source": "UNESCO Beijing Consensus Area 5; Jobin et al. (2019)",
    },
    "investigacion": {
        "label": "Investigación e innovación",
        "query": (
            "Research in educational AI, innovation, funding, research "
            "centers, academia-industry collaboration, piloting programs, "
            "impact evaluation"
        ),
        "source": "OECD Digital Education Outlook (2021)",
    },
    "equidad": {
        "label": "Equidad e inclusión",
        "query": (
            "Digital equity, inclusion, urban-rural divide, gender, access "
            "for vulnerable populations, compensatory mechanisms, "
            "socioeconomic disparities in AI education"
        ),
        "source": "UNESCO (general); Ng et al. (2021)",
    },
}

# ── BERTopic config (unsupervised analysis) ──
BERTOPIC_MIN_TOPIC_SIZE = 5
BERTOPIC_NR_TOPICS = "auto"  # let the algorithm decide

# ── Clustering config ──
CLUSTERING_METHODS = ["ward", "kmeans", "dbscan"]
SILHOUETTE_MIN_CLUSTERS = 2
SILHOUETTE_MAX_CLUSTERS = 6
