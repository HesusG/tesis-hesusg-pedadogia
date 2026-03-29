"""Build markdown versions of both homework documents for review."""

import sys
from pathlib import Path
from config import SCREENSHOTS_DIR, OUTPUT_DIR, check_banned_words

# ─── Paragraph text ───────────────────────────────────────────────

AI_PARAGRAPH = (
    "The Ministry of Education runs China's AI education system from top to bottom. "
    "It sets curricula at every school level and has pushed every major AI education "
    "directive since 2018, starting with the AI Innovation Action Plan that created "
    '"AI+X" programs at universities and expanded doctoral enrollment. In late 2024, '
    "the MOE told all K-12 schools to teach AI across every grade and picked 184 schools "
    "as pilot bases. By September 2025, every primary and secondary school in China had "
    "to offer at least 8 hours of AI instruction per year."
)

LANGUAGE_PARAGRAPH = (
    "The Ministry of Education controls language education at every level in China, "
    "from primary school English classes to the gaokao exam. English stays one of three "
    "required gaokao subjects, worth 150 out of 750 points, and students start learning "
    "it in third grade. The MOE also runs the State Language Commission and oversees the "
    "Center for Language Education and Cooperation. Its 2021 \"Double Reduction\" ban on "
    "for-profit K-9 tutoring reshaped how millions of students access language instruction, "
    "while recent gaokao reforms now let students sit the English exam twice a year."
)

# ─── Document metadata ────────────────────────────────────────────

AI_DOC = {
    "filename": "ai_education_homework.md",
    "title": "China's Government Institutions and AI Education Policy",
    "student_name": "Your Name",
    "research_topic": "How does the Chinese government regulate and promote artificial intelligence education?",
    "primary_institution": "Ministry of Education (教育部)",
    "primary_website": "https://www.moe.gov.cn/",
    "primary_screenshot": "moe_gov_cn.png",
    "secondary_institutions": [
        "Ministry of Science and Technology (科学技术部) — https://www.most.gov.cn/",
        "Cyberspace Administration of China (国家互联网信息办公室) — https://www.cac.gov.cn/",
    ],
    "paragraph": AI_PARAGRAPH,
}

LANGUAGE_DOC = {
    "filename": "language_education_homework.md",
    "title": "China's Government Institutions and Language Education Policy",
    "student_name": "Gaby",
    "research_topic": "How does the Chinese government manage and shape language education policy?",
    "primary_institution": "Ministry of Education (教育部)",
    "primary_website": "https://www.moe.gov.cn/",
    "primary_screenshot": "moe_gov_cn.png",
    "secondary_institutions": [
        "State Language Commission (国家语言文字工作委员会) — http://www.moe.gov.cn/jyb_sy/China_Language/",
        "Center for Language Education and Cooperation (中外语言交流合作中心) — https://www.chinese.cn/",
    ],
    "paragraph": LANGUAGE_PARAGRAPH,
}

MARKDOWN_TEMPLATE = """# {title}

**Student:** {student_name}

---

## Research Topic

{research_topic}

## Primary Institution

**{primary_institution}**

Website: {primary_website}

![Screenshot of {primary_institution} website]({screenshot_path})

## Other Relevant Institutions

{secondary_list}

## Summary Paragraph

{paragraph}

---

*Word count: {word_count}*
"""


def build_markdown(doc: dict):
    """Generate a markdown homework document."""
    paragraph = doc["paragraph"]
    word_count = len(paragraph.split())

    # Validate
    banned = check_banned_words(paragraph)
    if banned:
        print(f"  ERROR: Banned words found: {banned}")
        sys.exit(1)

    if word_count < 80 or word_count > 100:
        print(f"  WARNING: Word count is {word_count} (need 80-100)")

    screenshot_rel = f"../screenshots/{doc['primary_screenshot']}"
    secondary_list = "\n".join(f"- {inst}" for inst in doc["secondary_institutions"])

    md = MARKDOWN_TEMPLATE.format(
        title=doc["title"],
        student_name=doc["student_name"],
        research_topic=doc["research_topic"],
        primary_institution=doc["primary_institution"],
        primary_website=doc["primary_website"],
        screenshot_path=screenshot_rel,
        secondary_list=secondary_list,
        paragraph=paragraph,
        word_count=word_count,
    )

    out_path = OUTPUT_DIR / doc["filename"]
    out_path.write_text(md, encoding="utf-8")
    print(f"  Written: {out_path.name} ({word_count} words in paragraph)")
    return out_path


def main():
    print("=" * 60)
    print("Building markdown homework documents")
    print("=" * 60)

    for doc in [AI_DOC, LANGUAGE_DOC]:
        print(f"\n--- {doc['title']} ---")
        build_markdown(doc)

    print("\n" + "=" * 60)
    print("Done! Review the markdown files in output/")
    print("=" * 60)
    for f in sorted(OUTPUT_DIR.glob("*.md")):
        print(f"  {f.name}")


if __name__ == "__main__":
    main()
