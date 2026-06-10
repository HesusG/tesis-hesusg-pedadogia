"""Semantic proximity of policies to global templates vs. local-tradition lexicons.

Computes, for each policy document, the cosine similarity between the document
centroid and (a) curated lexicons of local philosophical-educational traditions
(Confucian, Pancasila) and (b) the global AI-education policy template vocabulary
(UNESCO/OECD-style principles). This operationalizes the "eco global o voz propia"
research question: do national policies speak the language of global templates or
of their own traditions?

Run: USE_LOCAL_EMBEDDINGS=1 python3 -m pipeline.lexicons
Output: web/data/lexicon_scores.json
"""
import json

import numpy as np
from scipy.spatial.distance import cosine

from .config import METADATA_FILE, WEB_DATA_DIR
from .embeddings import get_embedding_function
from .similarity import get_collection, get_policy_embedding

# Each lexicon is a set of descriptor sentences (not bare keywords) so the
# embedding captures the concept, not the token. Sources: Tan (2020, 2023),
# Wong & Wang (2021), Lee (1996), Li (2012) for the Confucian lexicon;
# Stranas KA (2020) for Pancasila; OECD (2019), UNESCO (2021, 2023) and the
# ASEAN Guide (2024) for the global template.
LEXICONS = {
    "confuciano": [
        "El maestro como ejemplar moral y autoridad ética que guía la formación del estudiante",
        "El aprendizaje como autocultivo y perfeccionamiento moral de la persona (xiushen)",
        "La educación para llegar a ser plenamente humano, formación del carácter virtuoso (junzi, ren)",
        "El esfuerzo y la perseverancia como vía del aprendizaje por encima del talento innato",
        "La armonía social y el respeto a la jerarquía en la relación maestro-discípulo",
        "El examen y el mérito académico como vía de movilidad y selección de los mejores",
        "La piedad filial, el respeto a los mayores y la transmisión de la tradición",
    ],
    "pancasila": [
        "Los valores de Pancasila como fundamento ético y filosófico de la nación",
        "La formación del carácter nacional y la identidad cultural del pueblo (karakter kebangsaan)",
        "La unidad en la diversidad y la justicia social para todo el pueblo",
        "La deliberación y el consenso comunitario como forma de decisión (musyawarah)",
        "La fe en Dios y la humanidad justa y civilizada como principios rectores",
        "La obra de los hijos de la nación y la soberanía tecnológica nacional",
    ],
    "plantilla_global": [
        "Transparencia y explicabilidad de los sistemas de inteligencia artificial",
        "Equidad, inclusión y no discriminación en el uso de la inteligencia artificial",
        "Privacidad y gobernanza de los datos personales de los estudiantes",
        "Rendición de cuentas, responsabilidad y supervisión humana de la IA",
        "Enfoque centrado en el ser humano para una inteligencia artificial confiable",
        "Seguridad, robustez y fiabilidad de los sistemas de inteligencia artificial",
        "Desarrollo de competencias digitales y alfabetización en IA para el siglo XXI",
        "Aprendizaje a lo largo de la vida y mejora de habilidades de la fuerza laboral",
    ],
}


def lexicon_embedding(embedding_fn, sentences: list[str]) -> np.ndarray:
    """Average embedding of the lexicon's descriptor sentences."""
    vectors = embedding_fn(sentences)
    return np.mean(np.asarray(vectors), axis=0)


def compute_lexicon_scores() -> dict:
    """Cosine similarity of each policy centroid to each lexicon centroid."""
    collection = get_collection()
    embedding_fn = get_embedding_function()

    with open(METADATA_FILE, encoding="utf-8") as f:
        metadata = json.load(f)

    lexicon_vectors = {
        name: lexicon_embedding(embedding_fn, sentences)
        for name, sentences in LEXICONS.items()
    }

    scores = {}
    for policy in metadata["policies"]:
        pid = policy["policy_id"]
        try:
            policy_vec = get_policy_embedding(collection, pid)
        except ValueError:
            continue
        scores[pid] = {
            name: float(1 - cosine(policy_vec, vec))
            for name, vec in lexicon_vectors.items()
        }
        # voice index: local-tradition proximity minus global-template proximity
        local = max(scores[pid]["confuciano"], scores[pid]["pancasila"])
        scores[pid]["indice_voz"] = float(local - scores[pid]["plantilla_global"])

    return scores


def main():
    scores = compute_lexicon_scores()
    WEB_DATA_DIR.mkdir(parents=True, exist_ok=True)
    output = WEB_DATA_DIR / "lexicon_scores.json"
    with open(output, "w", encoding="utf-8") as f:
        json.dump({"lexicons": LEXICONS, "scores": scores}, f, indent=2, ensure_ascii=False)
    print(f"✓ Lexicon scores for {len(scores)} policies → {output}")
    for pid, s in sorted(scores.items(), key=lambda kv: -kv[1]["indice_voz"]):
        print(f"  {pid:<34} conf={s['confuciano']:.3f} panc={s['pancasila']:.3f} "
              f"global={s['plantilla_global']:.3f} voz={s['indice_voz']:+.3f}")


if __name__ == "__main__":
    main()
