"""OpenRouter: cliente unificado + clasificación de un pasaje (SPIKE Fase 2).

Una sola API (OpenRouter) para todas las familias del panel. El clasificador
aplica el códebook pre-registrado (system prompt XML) y devuelve JSON estricto.
"""
import os
import re
import json

from openai import OpenAI

from .config import OPENROUTER_BASE_URL, CLASSIFIER_TEMPERATURE, load_codebook


def client():
    return OpenAI(base_url=OPENROUTER_BASE_URL, api_key=os.getenv("OPENROUTER_API_KEY"))


def build_system_prompt(cb: dict) -> str:
    """System prompt XML-tagged con el códebook pre-registrado."""
    rules = "\n".join(f"  - {r}" for r in cb["decision_rules"])
    return (
        "<rol>Eres un codificador experto de encuadre de gobernanza en política pública. "
        "Aplicas una rúbrica pre-registrada con rigor, no tu opinión.</rol>\n"
        "<tarea>Clasifica el PASAJE en un score ENTERO de -2 a +2 en el eje de gobernanza.</tarea>\n"
        "<rubrica>\n"
        f"POLO +2 (Estado cultiva/dirige, dézhì): {cb['pole_positive']}\n"
        f"POLO -2 (derechos limitan al Estado, liberal): {cb['pole_negative']}\n"
        "0 = neutral o no trata de la relación Estado-sociedad.\n"
        f"REGLAS DE DECISIÓN:\n{rules}\n"
        f"GÉNERO: {cb['genre_instruction']}\n"
        "</rubrica>\n"
        "<salida>Devuelve SOLO un objeto JSON: "
        '{"score": <entero -2..2>, "rationale": "<una frase>", "confidence": <0..1>}</salida>'
    )


def _parse(text: str) -> dict:
    try:
        return json.loads(text)
    except Exception:
        m = re.search(r"\{.*\}", text, re.DOTALL)
        if m:
            return json.loads(m.group(0))
        raise


def classify(model: str, passage: str, cb: dict | None = None,
             temperature: float = CLASSIFIER_TEMPERATURE) -> dict:
    """Clasifica un pasaje con un modelo vía OpenRouter. Robusto a modelos sin json mode."""
    cb = cb or load_codebook()
    cl = client()
    msgs = [
        {"role": "system", "content": build_system_prompt(cb)},
        {"role": "user", "content": f"PASAJE:\n{passage}\n\nResponde SOLO con el JSON."},
    ]
    last = None
    for rf in ({"type": "json_object"}, None):
        try:
            kw = dict(model=model, temperature=temperature, messages=msgs, max_tokens=400)
            if rf:
                kw["response_format"] = rf
            r = cl.chat.completions.create(**kw)
            out = _parse(r.choices[0].message.content)
            out["score"] = int(max(-2, min(2, round(float(out["score"])))))
            return out
        except Exception as e:  # noqa: BLE001
            last = e
    return {"error": str(last)}
