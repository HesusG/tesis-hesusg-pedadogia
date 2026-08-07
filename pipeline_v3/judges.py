"""OpenRouter: cliente unificado + clasificación de un pasaje (SPIKE Fase 2, robustecido en Fase 5).

Una sola API (OpenRouter) para todas las familias del panel. El clasificador
aplica el códebook pre-registrado (system prompt XML) y devuelve JSON estricto.

Fase 5 añade las tres garantías que el spec §5 exige para que la medición sea
reproducible: **caché en disco** de cada salida cruda (re-correr = replay, no
re-llamar), **reintentos** con backoff para los modelos intermitentes (glm, kimi),
y un **log de auditoría** inmutable (JSONL) con modelo, timestamp y hash del
códebook por clasificación.
"""
import os
import re
import json
import time
import hashlib
from datetime import datetime, timezone

from openai import OpenAI

from .config import (OPENROUTER_BASE_URL, CLASSIFIER_TEMPERATURE, CACHE_DIR,
                     CLASSIFIER_MAX_RETRIES, CLASSIFIER_BACKOFF_SEC,
                     CLASSIFIER_MAX_TOKENS, load_codebook)

CLASSIFY_CACHE_DIR = CACHE_DIR / "classifications"
AUDIT_LOG = CACHE_DIR / "audit_log.jsonl"


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


def codebook_hash(cb: dict) -> str:
    """Huella del códebook: si cambia la rúbrica, la caché se invalida sola."""
    return hashlib.sha256(
        json.dumps(cb, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()[:12]


def _cache_key(model: str, passage: str, cb_hash: str, temperature: float) -> str:
    raw = f"{model}|{temperature}|{cb_hash}|{passage}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]


def _parse(text: str) -> dict:
    try:
        return json.loads(text)
    except Exception:
        m = re.search(r"\{.*\}", text, re.DOTALL)
        if m:
            return json.loads(m.group(0))
        raise


def _audit(record: dict) -> None:
    AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
    with AUDIT_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def classify(model: str, passage: str, cb: dict | None = None,
             temperature: float = CLASSIFIER_TEMPERATURE,
             use_cache: bool = True) -> dict:
    """Clasifica un pasaje con un modelo vía OpenRouter.

    Robusto a modelos sin json mode (cae a texto libre + extracción de JSON) y a
    fallos intermitentes (reintentos con backoff). Cachea la salida cruda en disco:
    la misma (modelo, pasaje, códebook, temperatura) nunca se vuelve a pagar.
    """
    cb = cb or load_codebook()
    cbh = codebook_hash(cb)
    key = _cache_key(model, passage, cbh, temperature)
    cache_file = CLASSIFY_CACHE_DIR / f"{key}.json"

    if use_cache and cache_file.exists():
        hit = json.loads(cache_file.read_text(encoding="utf-8"))
        hit["_cached"] = True
        return hit

    cl = client()
    msgs = [
        {"role": "system", "content": build_system_prompt(cb)},
        {"role": "user", "content": f"PASAJE:\n{passage}\n\nResponde SOLO con el JSON."},
    ]
    last = None
    for attempt in range(CLASSIFIER_MAX_RETRIES):
        for rf in ({"type": "json_object"}, None):
            try:
                kw = dict(model=model, temperature=temperature, messages=msgs,
                          max_tokens=CLASSIFIER_MAX_TOKENS)
                if rf:
                    kw["response_format"] = rf
                r = cl.chat.completions.create(**kw)
                choice = r.choices[0]
                content = choice.message.content
                if not content:
                    # Modelo de razonamiento truncado antes de emitir la respuesta:
                    # error explícito y accionable, no un críptico 'NoneType'.
                    raise ValueError(
                        f"respuesta vacía (finish_reason={choice.finish_reason}); "
                        "sube CLASSIFIER_MAX_TOKENS")
                out = _parse(content)
                out["score"] = int(max(-2, min(2, round(float(out["score"])))))
                out["_model"] = model
                out["_codebook"] = cbh
                out["_ts"] = datetime.now(timezone.utc).isoformat()
                CLASSIFY_CACHE_DIR.mkdir(parents=True, exist_ok=True)
                cache_file.write_text(json.dumps(out, ensure_ascii=False, indent=2),
                                      encoding="utf-8")
                _audit({**{k: v for k, v in out.items() if k != "rationale"},
                        "cache_key": key, "attempt": attempt + 1})
                return out
            except Exception as e:  # noqa: BLE001
                last = e
        if attempt + 1 < CLASSIFIER_MAX_RETRIES:
            time.sleep(CLASSIFIER_BACKOFF_SEC * (2 ** attempt))

    err = {"error": str(last), "_model": model, "_codebook": cbh,
           "_ts": datetime.now(timezone.utc).isoformat()}
    _audit({**err, "cache_key": key, "attempt": CLASSIFIER_MAX_RETRIES})
    return err
