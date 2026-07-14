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

# ── Two-level China design ──
# Level 1 (cross-national): China represented by K-12 Guidance 2024 only
CHINA_CROSSNATIONAL_DOC = "china_k12_guidance_2024"
# Level 2 (longitudinal): all 7 docs scored individually
CHINA_LONGITUDINAL_DOCS = list(CHINA_DOCUMENTS.keys())

# Legacy composite group (for backward compatibility)
COMPOSITE_GROUPS = {
    "china": CHINA_LONGITUDINAL_DOCS,
}

REGION_COLORS = {
    "norteamerica": "#1565c0",
    "latinoamerica": "#388e3c",
    "europa": "#6a1b9a",
    "africa": "#e65100",
    "oceania": "#00838f",
    "asia": "#d32f2f",
}

# ── Stratified sampling for BERTopic ──
CHUNKS_PER_COUNTRY_CAP = 80

# ── Analysis dimensions (PRE-REGISTERED) ──
# 9 dimensions in 3 tiers (content, process, results).
# Derived EXCLUSIVELY from the literature review, NOT from reading the corpus.
# Committed to git BEFORE running any supervised analysis.
# The git history serves as the pre-registration record.
#
# Framework sources:
#   - OECD Education Policy Outlook (2021): Students, Institutions, System,
#     Governance, Evaluation categories
#   - UNESCO Beijing Consensus (2019): Areas 1-5
#   - Miao et al. (2021): curriculum, infrastructure, teacher support
#   - UNESCO Ethics Recommendation (2021): ethics principles
#   - OECD AI Principles (2019): accountability, transparency
#   - Bray & Thomas (1995): actor selection in comparative analysis
#   - Shipan & Volden (2012): diffusion agents
#   - Howlett & Ramesh (2003): policy cycle (evaluation phase)
#   - Long & Magerko (2020), Ng et al. (2021): AI literacy
#   - Mishra & Koehler (2006): TPACK for teacher knowledge
#
# Each dimension has a bilingual anchor paragraph (ES + EN) that gets
# embedded with the same model as the corpus. Cosine similarity between
# the anchor vector and each chunk vector = dimension score.
#
# IMPORTANT: Do NOT modify these anchors after ingesting documents.
# Any post-hoc refinement breaks the pre-registration and reintroduces
# the circular validation problem from v1.

DIMENSIONS = {
    # ── Tier 1: Content ──
    "curriculo": {
        "label": "Currículo e integración educativa",
        "tier": "content",
        "anchor_es": (
            "Este fragmento describe el contenido curricular de inteligencia "
            "artificial en el sistema educativo. Incluye la definición de "
            "competencias de IA que los estudiantes deben desarrollar, la "
            "integración de la IA como materia independiente o como componente "
            "transversal en otras asignaturas, y los niveles educativos en los "
            "que se implementa (primaria, secundaria, educación superior). "
            "Abarca también los estándares de aprendizaje, los marcos de "
            "competencias digitales y de alfabetización en IA, y las decisiones "
            "sobre si enseñar programación, pensamiento computacional, uso "
            "crítico de herramientas de IA o una combinación de estos enfoques."
        ),
        "anchor_en": (
            "This passage describes AI curriculum content in the education "
            "system. It includes the definition of AI competencies students "
            "must develop, integration of AI as a standalone subject or "
            "cross-curricular component, and the educational levels at which "
            "it is implemented (primary, secondary, higher education). It also "
            "covers learning standards, digital competency and AI literacy "
            "frameworks, and decisions about teaching programming, "
            "computational thinking, critical use of AI tools, or a "
            "combination of these approaches."
        ),
        "source": "OECD EPO 'Students'; Beijing area 2; Long & Magerko (2020)",
    },
    "formacion_docente": {
        "label": "Formación docente",
        "tier": "content",
        "anchor_es": (
            "Este fragmento aborda la preparación y capacitación de profesores "
            "para trabajar con inteligencia artificial en contextos educativos. "
            "Incluye programas de formación inicial y continua en competencias "
            "de IA para docentes, certificaciones profesionales, marcos de "
            "competencias pedagógicas digitales y requisitos de actualización. "
            "Describe quién diseña e imparte la formación, qué instituciones "
            "participan (universidades, centros de formación, empresas "
            "tecnológicas) y cómo se evalúa la competencia docente en IA. "
            "Comprende también la provisión de recursos didácticos, guías "
            "pedagógicas y comunidades de práctica para educadores."
        ),
        "anchor_en": (
            "This passage addresses the preparation and training of teachers "
            "to work with artificial intelligence in educational settings. It "
            "includes pre-service and in-service training programs in AI "
            "competencies for educators, professional certifications, digital "
            "pedagogical competency frameworks, and continuing education "
            "requirements. It describes who designs and delivers the training, "
            "which institutions participate, and how teacher AI competency is "
            "assessed. It also covers the provision of teaching resources, "
            "pedagogical guides, and communities of practice for educators."
        ),
        "source": "OECD EPO 'Institutions'; Beijing area 3; Mishra & Koehler (2006)",
    },
    "infraestructura": {
        "label": "Infraestructura y acceso",
        "tier": "content",
        "anchor_es": (
            "Este fragmento describe la infraestructura tecnológica y digital "
            "necesaria para la integración de la inteligencia artificial en la "
            "educación. Incluye inversiones en conectividad a internet en "
            "escuelas, equipamiento informático (computadoras, tabletas, "
            "laboratorios), plataformas digitales educativas, servicios en la "
            "nube y centros de datos. Abarca también la disponibilidad de "
            "electricidad, ancho de banda, software educativo con componentes "
            "de IA, y los planes de adquisición, mantenimiento y actualización "
            "de recursos tecnológicos en instituciones educativas."
        ),
        "anchor_en": (
            "This passage describes the technological and digital "
            "infrastructure needed for integrating artificial intelligence in "
            "education. It includes investments in school internet "
            "connectivity, computing equipment (computers, tablets, labs), "
            "educational digital platforms, cloud services, and data centers. "
            "It also covers electricity availability, bandwidth, AI-enabled "
            "educational software, and plans for procurement, maintenance, and "
            "upgrading of technological resources in educational institutions."
        ),
        "source": "OECD EPO 'System'; Beijing area 1",
    },
    "investigacion": {
        "label": "Investigación e innovación",
        "tier": "content",
        "anchor_es": (
            "Este fragmento se refiere a la producción de conocimiento sobre "
            "inteligencia artificial aplicada a la educación. Incluye la "
            "creación de centros de investigación dedicados a IA educativa, "
            "programas de financiamiento para investigación, vínculos de "
            "colaboración entre universidades y empresas tecnológicas, y "
            "prioridades de investigación y desarrollo (I+D). Abarca "
            "convocatorias de proyectos, publicaciones académicas, "
            "transferencia de resultados de investigación al aula, y la "
            "formación de investigadores especializados en la intersección "
            "entre IA y pedagogía."
        ),
        "anchor_en": (
            "This passage refers to the production of knowledge about "
            "artificial intelligence applied to education. It includes the "
            "creation of research centers dedicated to educational AI, "
            "research funding programs, university-industry collaboration "
            "links, and R&D priorities. It covers project calls, academic "
            "publications, transfer of research results to the classroom, and "
            "training of researchers specialized in the intersection of AI "
            "and pedagogy."
        ),
        "source": "Beijing area 5; OECD Digital Education Outlook (2021)",
    },

    # ── Tier 2: Process ──
    "gobernanza": {
        "label": "Gobernanza y regulación",
        "tier": "process",
        "anchor_es": (
            "Este fragmento describe las estructuras de gobernanza para la "
            "inteligencia artificial en educación. Incluye la identificación "
            "del ministerio u organismo responsable de liderar la política, la "
            "existencia de comités interinstitucionales o agencias "
            "especializadas, los marcos regulatorios y normativos que enmarcan "
            "el uso de IA en escuelas, y los mecanismos de coordinación entre "
            "niveles de gobierno (federal, estatal, municipal). Comprende "
            "también la asignación presupuestaria, los instrumentos legales "
            "(leyes, decretos, lineamientos) y las estructuras de toma de "
            "decisiones sobre tecnología educativa."
        ),
        "anchor_en": (
            "This passage describes governance structures for artificial "
            "intelligence in education. It includes the identification of the "
            "ministry or agency responsible for leading the policy, the "
            "existence of inter-institutional committees or specialized "
            "agencies, regulatory and normative frameworks governing AI use in "
            "schools, and coordination mechanisms between levels of government "
            "(federal, state, municipal). It also covers budget allocation, "
            "legal instruments (laws, decrees, guidelines), and decision-making "
            "structures for educational technology."
        ),
        "source": "OECD EPO 'Governance'; Howlett & Ramesh (2003)",
    },
    "participacion_actores": {
        "label": "Participación de actores",
        "tier": "process",
        "anchor_es": (
            "Este fragmento describe la participación de diversos actores en "
            "la formulación de políticas de inteligencia artificial en "
            "educación. Incluye mecanismos vinculantes de consulta pública, "
            "foros de diálogo, mesas de trabajo y procesos participativos con "
            "incorporación formal de recomendaciones. Identifica los actores "
            "involucrados: sociedad civil, sector empresarial y tecnológico, "
            "comunidad académica, sindicatos de docentes, organizaciones de "
            "padres de familia, estudiantes y organismos internacionales. "
            "Describe también alianzas público-privadas, la representación "
            "formal de actores en órganos de decisión y el papel de "
            "organizaciones como UNESCO y OCDE en la orientación de las "
            "políticas nacionales."
        ),
        "anchor_en": (
            "This passage describes the participation of diverse stakeholders "
            "in the formulation of artificial intelligence education policies. "
            "It includes binding public consultation mechanisms, dialogue "
            "forums, working groups, and participatory processes with formal "
            "incorporation of recommendations. It identifies the actors "
            "involved: civil society, the business and technology sector, "
            "academia, teacher unions, parent organizations, students, and "
            "international organizations. It also describes public-private "
            "partnerships, formal stakeholder representation in decision-making "
            "bodies, and the role of UNESCO and OECD in shaping national "
            "policies."
        ),
        "source": "Bray & Thomas (1995); Shipan & Volden (2012)",
    },

    # ── Tier 3: Results ──
    "etica": {
        "label": "Ética y rendición de cuentas",
        "tier": "results",
        "anchor_es": (
            "Este fragmento aborda los principios éticos y los mecanismos de "
            "rendición de cuentas para el uso de inteligencia artificial en "
            "educación. Incluye directrices sobre transparencia algorítmica, "
            "protección de datos personales de estudiantes y docentes, "
            "prevención del sesgo algorítmico, y supervisión humana de "
            "decisiones automatizadas. Describe mecanismos de auditoría, "
            "organismos de vigilancia, sanciones por uso indebido de IA en "
            "contextos educativos, y procedimientos para que estudiantes, "
            "docentes o familias impugnen decisiones tomadas por sistemas "
            "de IA."
        ),
        "anchor_en": (
            "This passage addresses ethical principles and accountability "
            "mechanisms for the use of artificial intelligence in education. "
            "It includes guidelines on algorithmic transparency, protection "
            "of student and teacher personal data, prevention of algorithmic "
            "bias, and human oversight of automated decisions. It describes "
            "audit mechanisms, oversight bodies, sanctions for misuse of AI in "
            "educational settings, and procedures for students, teachers, or "
            "families to challenge decisions made by AI systems."
        ),
        "source": "UNESCO Ethics Recommendation (2021); OECD AI Principles (2019)",
    },
    "equidad": {
        "label": "Equidad e inclusión",
        "tier": "results",
        "anchor_es": (
            "Este fragmento describe las medidas para garantizar el acceso "
            "equitativo a la inteligencia artificial en educación. Incluye "
            "políticas dirigidas a reducir brechas digitales entre zonas "
            "urbanas y rurales, entre escuelas públicas y privadas, y entre "
            "poblaciones según género, etnia, nivel socioeconómico o condición "
            "de discapacidad. Abarca programas de inclusión digital, subsidios "
            "para tecnología educativa en comunidades marginadas, adaptaciones "
            "para estudiantes con necesidades especiales, y estrategias para "
            "prevenir que la IA reproduzca o amplíe desigualdades existentes "
            "en el sistema educativo."
        ),
        "anchor_en": (
            "This passage describes measures to ensure equitable access to "
            "artificial intelligence in education. It includes policies aimed "
            "at reducing digital divides between urban and rural areas, between "
            "public and private schools, and among populations by gender, "
            "ethnicity, socioeconomic status, or disability. It covers digital "
            "inclusion programs, subsidies for educational technology in "
            "marginalized communities, accommodations for students with "
            "special needs, and strategies to prevent AI from reproducing or "
            "amplifying existing inequalities in the education system."
        ),
        "source": "OECD EPO 'Equity'; Beijing area 4",
    },
    "metas_evaluacion": {
        "label": "Metas y evaluación",
        "tier": "results",
        "anchor_es": (
            "Este fragmento describe los objetivos cuantificables y los "
            "mecanismos de evaluación establecidos en la política de "
            "inteligencia artificial en educación. Incluye metas numéricas "
            "(por ejemplo, capacitar a 500,000 docentes para 2025 o lograr "
            "cobertura de internet en el 100% de las escuelas), indicadores "
            "de desempeño, plazos de cumplimiento, y mecanismos de monitoreo "
            "y seguimiento. Describe también cláusulas de revisión periódica "
            "de la política, evaluaciones de impacto programadas, y la "
            "designación de responsables de reportar avances."
        ),
        "anchor_en": (
            "This passage describes quantifiable objectives and evaluation "
            "mechanisms established in AI education policy. It includes "
            "numerical targets (e.g., train 500,000 teachers by 2025 or "
            "achieve internet coverage in 100% of schools), performance "
            "indicators, compliance deadlines, and monitoring and follow-up "
            "mechanisms. It also describes periodic policy review clauses, "
            "scheduled impact evaluations, and the designation of officials "
            "responsible for reporting progress."
        ),
        "source": "Howlett & Ramesh (2003) evaluation phase; OECD EPO 'Evaluation'",
    },
}

# Legacy compatibility: build query strings from anchors for scoring
for _dim in DIMENSIONS.values():
    _dim["query"] = _dim["anchor_es"]

# ── BERTopic config (unsupervised analysis) ──
BERTOPIC_MIN_TOPIC_SIZE = 5
BERTOPIC_NR_TOPICS = "auto"  # let the algorithm decide

# Sensitivity sweep grid (report all combinations, pick best)
BERTOPIC_SENSITIVITY_GRID = {
    "min_topic_size": [3, 5, 8],
    "n_neighbors": [5, 10, 15],
}
BERTOPIC_MAX_OUTLIER_RATIO = 0.40  # reject configs above this

# ── Clustering config ──
CLUSTERING_METHODS = ["ward", "kmeans", "dbscan"]
SILHOUETTE_MIN_CLUSTERS = 2
SILHOUETTE_MAX_CLUSTERS = 6

# ── Dimension scoring config ──
SCORING_TOP_K_PERCENTILE = 0.10  # use top 10% of chunks per doc
SCORING_BILINGUAL_STRATEGY = "average"  # average ES+EN anchor vectors

# ════════════════════════════════════════════════════════════════════
#  MVP: Confucian concept axes (Kozlowski-style bipolar projection)
# ════════════════════════════════════════════════════════════════════
# Read policies from the ACTUAL stored collection. NOTE: the populated
# collection is "politicas_ia_educacion" (NO "_v2" suffix); COLLECTION_NAME
# above points at a name that does not exist on disk.
POLICY_READ_COLLECTION_NAME = "politicas_ia_educacion"
ANALECTS_COLLECTION_NAME = "analectas_confucio"
ANALECTS_SOURCE_FILE = PROJECT_ROOT / "corpus" / "analects" / "analects_legge_en.txt"
CONFUCIAN_MVP_JSON = WEB_DATA_DIR / "confucian_mvp.json"

# The China policy is NOT in the stored v1 collection; ingest it on demand
# from its raw English translation so the MVP contrast includes China.
CHINA_MVP_POLICY = {
    "policy_id": "china_ngaidp_2017",
    "raw_file": RAW_DIR / "china" / "3_new_gen_ai_development_plan_2017_en.txt",
    "country": "china", "region": "asia", "year": 2017, "language": "en",
}

# Three MVP policies (max contrast) + the legalistic negative control.
MVP_POLICY_IDS = [
    "china_ngaidp_2017",
    "colombia_conpes_3975_2019",
    "canada_pan_canadian_ai_strategy_2017",
]
MVP_CONTROL_NEG_POLICY_ID = "eu_ai_act_2024"  # command-and-control legal text

# Pre-registered bipolar Confucian axes. Each axis is a DIRECTION in embedding
# space: axis = normalize(mean(pos_anchors) - mean(neg_anchors)). A document's
# score on an axis is the projection of its chunk vectors onto that direction.
# PRE-REGISTRATION: do NOT modify these anchors after computing results.
CONFUCIAN_AXES = {
    "ren": {
        "label": "Benevolencia", "zh": "仁", "pinyin": "rén",
        "pos_pole": "centrado en la persona", "neg_pole": "eficiencia instrumental",
        "pos_anchors_en": [
            "Governing and educating with benevolence and humaneness, caring for each person's dignity and wellbeing.",
            "The benevolent person loves others and puts people at the center of every decision.",
        ],
        "pos_anchors_es": [
            "Gobernar y educar con benevolencia y humanidad, cuidando la dignidad y el bienestar de cada persona.",
            "La persona benevolente ama a los demás y pone a las personas en el centro de cada decisión.",
        ],
        "neg_anchors_en": [
            "Treating people as instruments for efficiency, output, and economic productivity.",
            "Optimizing systems for performance and profit without regard for human dignity.",
        ],
        "neg_anchors_es": [
            "Tratar a las personas como instrumentos para la eficiencia, la producción y la productividad económica.",
            "Optimizar los sistemas por rendimiento y ganancia sin considerar la dignidad humana.",
        ],
    },
    "li": {
        "label": "Ritual y propiedad", "zh": "礼", "pinyin": "lǐ",
        "pos_pole": "normas y estándares", "neg_pole": "sin normas",
        "pos_anchors_en": [
            "Proper conduct guided by ritual, established norms, codes of conduct, and shared standards of appropriate behavior.",
            "Following rites, protocols, and rules of propriety that structure how people should act.",
        ],
        "pos_anchors_es": [
            "Conducta correcta guiada por el ritual, las normas establecidas, los códigos de conducta y los estándares compartidos.",
            "Seguir ritos, protocolos y reglas de propiedad que estructuran cómo deben actuar las personas.",
        ],
        "neg_anchors_en": [
            "Acting without shared norms, protocols, or codes of conduct; improvised behavior with no rules.",
            "Rejecting formal standards and established procedures in favor of ad hoc action.",
        ],
        "neg_anchors_es": [
            "Actuar sin normas compartidas, protocolos ni códigos de conducta; comportamiento improvisado y sin reglas.",
            "Rechazar los estándares formales y los procedimientos establecidos en favor de la acción improvisada.",
        ],
    },
    "yi": {
        "label": "Rectitud", "zh": "义", "pinyin": "yì",
        "pos_pole": "lo justo", "neg_pole": "el provecho",
        "pos_anchors_en": [
            "Doing what is morally right and just regardless of profit or advantage; upholding justice and moral duty.",
            "Choosing the righteous course over personal gain.",
        ],
        "pos_anchors_es": [
            "Hacer lo que es moralmente correcto y justo sin importar el beneficio o la ventaja; sostener la justicia y el deber moral.",
            "Elegir el camino recto por encima del provecho personal.",
        ],
        "neg_anchors_en": [
            "Pursuing profit, self-interest, and advantage as the guide to action.",
            "Deciding by financial benefit and personal gain rather than by what is right.",
        ],
        "neg_anchors_es": [
            "Perseguir el beneficio, el interés propio y la ventaja como guía de la acción.",
            "Decidir por el beneficio económico y la ganancia personal en vez de por lo correcto.",
        ],
    },
    "xiushen": {
        "label": "Cultivo de sí mismo", "zh": "修身", "pinyin": "xiūshēn",
        "pos_pole": "formación del carácter", "neg_pole": "credencial instrumental",
        "pos_anchors_en": [
            "Lifelong moral self-cultivation, character formation, reflection, and self-improvement to become a better person.",
            "Cultivating virtue and one's own character through continuous learning and self-examination.",
        ],
        "pos_anchors_es": [
            "Cultivo moral de sí mismo a lo largo de la vida, formación del carácter, reflexión y mejora personal para ser mejor persona.",
            "Cultivar la virtud y el propio carácter mediante el aprendizaje continuo y el autoexamen.",
        ],
        "neg_anchors_en": [
            "Acquiring credentials and technical skills only for external reward, status, and employment.",
            "Training merely to pass exams and gain qualifications, without moral or character growth.",
        ],
        "neg_anchors_es": [
            "Adquirir credenciales y habilidades técnicas solo por la recompensa externa, el estatus y el empleo.",
            "Formarse únicamente para aprobar exámenes y obtener títulos, sin crecimiento moral ni del carácter.",
        ],
    },
    "dezhi_fa": {
        "label": "Gobernar por virtud vs. por ley", "zh": "德治", "pinyin": "dézhì↔fǎ",
        "pos_pole": "德治 gobierno por virtud", "neg_pole": "法 gobierno por ley",
        "pos_anchors_en": [
            "Governing by moral virtue and example, leading people through ethics and cultivation so they develop conscience and correct themselves.",
            "Rule by virtue: the state guides society by moral example rather than coercion.",
        ],
        "pos_anchors_es": [
            "Gobernar por la virtud moral y el ejemplo, guiando a las personas mediante la ética y el cultivo para que desarrollen conciencia y se corrijan a sí mismas.",
            "Gobierno por virtud: el Estado guía a la sociedad con el ejemplo moral más que con la coerción.",
        ],
        "neg_anchors_en": [
            "Governing by strict law, coercion, punishment, sanctions, and mandatory command-and-control enforcement.",
            "Rule by law: compelling behavior through binding regulation, penalties, and prohibitions.",
        ],
        "neg_anchors_es": [
            "Gobernar por la ley estricta, la coerción, el castigo, las sanciones y la aplicación obligatoria de mando y control.",
            "Gobierno por la ley: obligar la conducta mediante regulación vinculante, penalizaciones y prohibiciones.",
        ],
    },
    "he": {
        "label": "Armonía", "zh": "和", "pinyin": "hé",
        "pos_pole": "bien colectivo", "neg_pole": "autonomía individual",
        "pos_anchors_en": [
            "Social harmony, collective wellbeing, concord, unity, and the common good of the community.",
            "Prioritizing social stability and the harmony of the whole society.",
        ],
        "pos_anchors_es": [
            "Armonía social, bienestar colectivo, concordia, unidad y bien común de la comunidad.",
            "Priorizar la estabilidad social y la armonía del conjunto de la sociedad.",
        ],
        "neg_anchors_en": [
            "Individual autonomy, competition, pluralism, and the primacy of personal rights and freedom over the collective.",
            "Emphasizing individual liberty, dissent, and personal choice over collective concord.",
        ],
        "neg_anchors_es": [
            "Autonomía individual, competencia, pluralismo y primacía de los derechos y la libertad personales sobre el colectivo.",
            "Enfatizar la libertad individual, el disenso y la elección personal por encima de la concordia colectiva.",
        ],
    },
    "zhi": {
        "label": "Sabiduría", "zh": "智", "pinyin": "zhì",
        "pos_pole": "discernimiento", "neg_pole": "ignorancia",
        "pos_anchors_en": [
            "Wisdom and practical knowledge; knowing right from wrong and understanding people.",
            "The wise person discerns what is true and acts with good judgment.",
        ],
        "pos_anchors_es": [
            "Sabiduría y conocimiento práctico; distinguir lo correcto de lo incorrecto y comprender a las personas.",
            "La persona sabia discierne lo verdadero y actúa con buen juicio.",
        ],
        "neg_anchors_en": [
            "Ignorance, folly, and acting without understanding or discernment.",
            "Deciding blindly, without knowledge or careful judgment.",
        ],
        "neg_anchors_es": [
            "Ignorancia, insensatez y actuar sin comprensión ni discernimiento.",
            "Decidir a ciegas, sin conocimiento ni juicio cuidadoso.",
        ],
    },
    "xin": {
        "label": "Confiabilidad", "zh": "信", "pinyin": "xìn",
        "pos_pole": "buena fe", "neg_pole": "engaño",
        "pos_anchors_en": [
            "Trustworthiness, sincerity, and keeping one's word; good faith and reliability.",
            "A trustworthy person honors commitments and can be relied upon.",
        ],
        "pos_anchors_es": [
            "Confiabilidad, sinceridad y cumplir la palabra dada; buena fe y fiabilidad.",
            "La persona confiable honra sus compromisos y merece confianza.",
        ],
        "neg_anchors_en": [
            "Deceit, broken promises, and bad faith; being unreliable and dishonest.",
            "Manipulation and disregard for one's given word.",
        ],
        "neg_anchors_es": [
            "Engaño, promesas rotas y mala fe; ser poco fiable y deshonesto.",
            "Manipulación y desprecio por la palabra dada.",
        ],
    },
    "xue": {
        "label": "Aprendizaje", "zh": "学", "pinyin": "xué",
        "pos_pole": "estudio devoto", "neg_pole": "sin estudio",
        "pos_anchors_en": [
            "Devoted study and lifelong learning; loving to learn and constantly practicing what one learns.",
            "Setting one's heart on learning and pursuing knowledge throughout life.",
        ],
        "pos_anchors_es": [
            "Estudio devoto y aprendizaje a lo largo de la vida; amar el aprendizaje y practicar constantemente lo aprendido.",
            "Poner el corazón en el aprendizaje y buscar el conocimiento toda la vida.",
        ],
        "neg_anchors_en": [
            "Neglecting study, refusing to learn, and remaining in ignorance.",
            "Indifference to knowledge and to improving one's understanding.",
        ],
        "neg_anchors_es": [
            "Descuidar el estudio, negarse a aprender y permanecer en la ignorancia.",
            "Indiferencia hacia el conocimiento y hacia mejorar la propia comprensión.",
        ],
    },
}

# A/B test: three candidate axis sets, scored over the same Analects-grounded anchors.
AXIS_SETS = {
    "tuned6": ["ren", "li", "yi", "xiushen", "dezhi_fa", "he"],
    "edu7":   ["ren", "li", "yi", "xiushen", "dezhi_fa", "he", "xue"],
    "canon5": ["ren", "yi", "li", "zhi", "xin"],
}
