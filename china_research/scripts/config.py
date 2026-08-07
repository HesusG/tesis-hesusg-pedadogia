"""Central configuration for the Chinese education policy project."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

# Directories
DOWNLOADS_DIR = PROJECT_ROOT / "downloads"
TRANSLATIONS_DIR = PROJECT_ROOT / "translations"
SCREENSHOTS_DIR = PROJECT_ROOT / "screenshots"
OUTPUT_DIR = PROJECT_ROOT / "output"

for d in [DOWNLOADS_DIR, TRANSLATIONS_DIR, SCREENSHOTS_DIR, OUTPUT_DIR]:
    d.mkdir(exist_ok=True)

# Together.ai API config
TOGETHER_API_BASE = "https://api.together.xyz/v1"
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY", "")
PRIMARY_MODEL = "Qwen/Qwen2.5-72B-Instruct"
FALLBACK_MODEL = "deepseek-ai/DeepSeek-V3"
TRANSLATION_TEMPERATURE = 0.3

# Policy documents to download
POLICY_DOCUMENTS = [
    {
        "id": "1",
        "slug": "ai_innovation_action_plan_2018",
        "title": "AI Innovation Action Plan for Higher Education",
        "year": 2018,
        "source": "MOE",
        "url": "https://www.moe.gov.cn/srcsite/A16/s7062/201804/t20180410_332722.html",
    },
    {
        "id": "2",
        "slug": "generative_ai_interim_measures_2023",
        "title": "Interim Measures for Generative AI Services",
        "year": 2023,
        "source": "CAC",
        "url": "https://www.cac.gov.cn/2023-07/13/c_1690898327029107.htm",
    },
    {
        "id": "3",
        "slug": "new_gen_ai_development_plan_2017",
        "title": "New Generation AI Development Plan",
        "year": 2017,
        "source": "State Council",
        "url": "https://www.gov.cn/zhengce/content/2017-07/20/content_5211996.htm",
    },
    {
        "id": "4",
        "slug": "k12_ai_education_guidance_2024",
        "title": "K-12 AI Education Guidance",
        "year": 2024,
        "source": "MOE",
        "url": "https://www.moe.gov.cn/srcsite/A06/s3321/202412/t20241202_1165500.html",
    },
    {
        "id": "5",
        "slug": "184_ai_education_base_schools_2024",
        "title": "184 AI Education Base Schools",
        "year": 2024,
        "source": "MOE",
        "url": "https://www.moe.gov.cn/srcsite/A06/s3321/202402/t20240223_1116386.html",
    },
    {
        "id": "6",
        "slug": "accelerating_education_digitalization_2025",
        "title": "Accelerating Education Digitalization",
        "year": 2025,
        "source": "MOE+9",
        "url": "https://www.moe.gov.cn/srcsite/A01/s7048/202504/t20250416_1187476.html",
    },
    {
        "id": "7",
        "slug": "smart_education_strategy_2025",
        "title": "Smart Education White Paper / Strategy 2.0",
        "year": 2025,
        "source": "MOE",
        "url": "https://www.moe.gov.cn/srcsite/A16/s3342/202505/t20250507_1189603.html",
    },
]

# Screenshots to capture
SCREENSHOT_TARGETS = [
    {
        "name": "moe_gov_cn",
        "url": "https://www.moe.gov.cn/",
        "used_in": ["ai", "language"],
    },
    {
        "name": "moe_gov_cn_en",
        "url": "http://en.moe.gov.cn/",
        "used_in": ["ai", "language"],
    },
    {
        "name": "most_gov_cn",
        "url": "https://www.most.gov.cn/",
        "used_in": ["ai"],
    },
    {
        "name": "cac_gov_cn",
        "url": "https://www.cac.gov.cn/",
        "used_in": ["ai"],
    },
    {
        "name": "chinese_cn",
        "url": "https://www.chinese.cn/",
        "used_in": ["language"],
    },
    {
        "name": "slc_page",
        "url": "http://www.moe.gov.cn/jyb_sy/China_Language/",
        "used_in": ["language"],
    },
]

# Banned AI-slop words (lowercase for checking)
BANNED_WORDS = {
    "groundbreaking", "cutting-edge", "game-changing", "revolutionary",
    "transformative", "unprecedented", "paradigm shift", "paradigm-shifting",
    "synergy", "synergies", "leverage", "leveraging", "leveraged",
    "holistic", "robust", "seamless", "seamlessly", "pivotal",
    # "innovative", "innovation", "innovating" — excluded, appears in real policy names
    "spearhead", "spearheading", "spearheaded",
    "trailblazing", "trailblazer",
    "empower", "empowering", "empowered", "empowerment",
    "foster", "fostering", "fostered",
    "harness", "harnessing", "harnessed",
    "delve", "delving", "delved",
    "navigate", "navigating", "navigated",  # metaphorical use
    "landscape",  # metaphorical use
    "tapestry", "vibrant tapestry",
    "beacon", "beacons",
    "cornerstone", "cornerstones",
    "testament",
    "multifaceted",
    "comprehensive",  # overused filler
    "underscore", "underscores", "underscoring",
    "noteworthy", "notably",
    "realm", "realms",
    "endeavor", "endeavors", "endeavour", "endeavours",
    "embark", "embarking", "embarked",
    "poised",
    "reshaping",
    "bolster", "bolstering", "bolstered",
    "advent",
    "commendable",
    "intricate", "intricacies",
    "nuanced",
    "ever-evolving",
    "cutting edge",
    "in today's world",
    "it is important to note",
    "it's important to note",
    "it is worth noting",
    "in conclusion",
    "plays a crucial role",
    "plays a pivotal role",
    "at the forefront",
    "a testament to",
    "serves as a",
}


def check_banned_words(text: str) -> list[str]:
    """Return list of banned words/phrases found in text."""
    lower = text.lower()
    found = []
    for word in BANNED_WORDS:
        if word in lower:
            found.append(word)
    return found
