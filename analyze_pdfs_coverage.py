from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader


WORKSPACE = Path(__file__).resolve().parent


STOPWORDS = {
    # PL (minimalny zestaw + typowe słowa z prezentacji/testów)
    "i",
    "oraz",
    "a",
    "ale",
    "albo",
    "lub",
    "że",
    "to",
    "te",
    "ta",
    "ten",
    "tę",
    "tych",
    "tym",
    "w",
    "we",
    "na",
    "do",
    "od",
    "dla",
    "po",
    "pod",
    "nad",
    "z",
    "ze",
    "o",
    "u",
    "jak",
    "jaki",
    "jaka",
    "jakie",
    "czy",
    "co",
    "kiedy",
    "gdzie",
    "który",
    "która",
    "które",
    "których",
    "którym",
    "się",
    "nie",
    "tak",
    "taka",
    "takie",
    "tego",
    "tej",
    "temu",
    "jest",
    "są",
    "być",
    "bywa",
    "będzie",
    "będą",
    "może",
    "można",
    "np",
    "itp",
    "etc",
    "przykład",
    "przyklad",
    "zadanie",
    "pytanie",
    "test",
    # EN (typowe w slajdach)
    "the",
    "and",
    "or",
    "a",
    "an",
    "to",
    "of",
    "in",
    "on",
    "for",
    "with",
    "as",
    "is",
    "are",
    "be",
    "this",
    "that",
    "these",
    "those",
    "from",
    "by",
    "at",
    "it",
    "its",
    "into",
    "about",
    "example",
    "examples",
    "python",
}


TOKEN_RE = re.compile(r"[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż_]{2,}")


@dataclass(frozen=True)
class DocStats:
    name: str
    text_len: int
    tokens: Counter[str]


def extract_pdf_text(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    parts: list[str] = []
    for page in reader.pages:
        txt = page.extract_text() or ""
        if txt:
            parts.append(txt)
    return "\n".join(parts)


def normalize_text(s: str) -> str:
    # ujednolicenie spacji + minusów/dashy
    s = s.replace("\u00ad", "")  # soft hyphen
    s = s.replace("\u2013", "-").replace("\u2014", "-")
    s = re.sub(r"[ \t]+", " ", s)
    return s


def tokenize(s: str) -> list[str]:
    s = normalize_text(s).lower()
    tokens = TOKEN_RE.findall(s)
    out: list[str] = []
    for t in tokens:
        if t in STOPWORDS:
            continue
        if len(t) <= 2:
            continue
        out.append(t)
    return out


def cosine_similarity(a: Counter[str], b: Counter[str]) -> float:
    if not a or not b:
        return 0.0
    dot = 0.0
    for k, va in a.items():
        vb = b.get(k)
        if vb:
            dot += va * vb
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def top_keywords(counter: Counter[str], *, k: int = 60, min_len: int = 3) -> list[tuple[str, int]]:
    items = [(t, c) for (t, c) in counter.items() if len(t) >= min_len]
    items.sort(key=lambda x: (-x[1], x[0]))
    return items[:k]


def compute_coverage(test_tokens: Counter[str], lecture_tokens: Counter[str]) -> float:
    # Pokrycie = odsetek unikalnych tokenów testu (z sensowną częstością),
    # które występują w wykładach.
    # Próg 2 usuwa „śmieci”/pojedyncze literówki.
    test_set = {t for t, c in test_tokens.items() if c >= 2 and len(t) >= 3}
    if not test_set:
        test_set = {t for t, c in test_tokens.items() if c >= 1 and len(t) >= 3}
    if not test_set:
        return 0.0
    lec_set = {t for t, c in lecture_tokens.items() if c >= 1 and len(t) >= 3}
    inter = len(test_set & lec_set)
    return 100.0 * inter / len(test_set)


def main() -> None:
    pdfs = sorted(WORKSPACE.glob("W[0-9].pdf")) + sorted(WORKSPACE.glob("W[0-9][0-9].pdf"))
    pdfs = [p for p in pdfs if p.is_file()]
    test_pdf = WORKSPACE / "test_python.pdf"

    if not test_pdf.exists():
        raise SystemExit("Brak test_python.pdf w katalogu głównym.")
    if not pdfs:
        raise SystemExit("Nie znaleziono PDF-ów W1..W11 w katalogu głównym.")

    # Ekstrakcja
    test_text = extract_pdf_text(test_pdf)
    test_stats = DocStats(
        name=test_pdf.name,
        text_len=len(test_text),
        tokens=Counter(tokenize(test_text)),
    )

    lecture_docs: list[DocStats] = []
    lecture_all = Counter()
    for p in pdfs:
        txt = extract_pdf_text(p)
        c = Counter(tokenize(txt))
        lecture_docs.append(DocStats(name=p.name, text_len=len(txt), tokens=c))
        lecture_all.update(c)

    # Metryki
    overall_cov = compute_coverage(test_stats.tokens, lecture_all)
    overall_cos = cosine_similarity(test_stats.tokens, lecture_all) * 100.0

    # Braki (top z testu, których nie ma w wykładach)
    lecture_vocab = set(lecture_all.keys())
    missing = [(t, c) for (t, c) in test_stats.tokens.items() if t not in lecture_vocab and len(t) >= 3]
    missing.sort(key=lambda x: (-x[1], x[0]))

    per_doc = []
    for d in lecture_docs:
        cov = compute_coverage(test_stats.tokens, d.tokens)
        cos = cosine_similarity(test_stats.tokens, d.tokens) * 100.0
        per_doc.append((d.name, cov, cos, sum(d.tokens.values())))
    per_doc.sort(key=lambda x: (-x[1], -x[2], x[0]))

    # Raport
    report = []
    report.append("# Raport pokrycia: W1–W11 vs test_python.pdf\n")
    report.append(f"- Test: **{test_stats.name}** (znaki: {test_stats.text_len:,}, tokeny: {sum(test_stats.tokens.values()):,})")
    report.append(f"- Wykłady: **{len(lecture_docs)} plików** (tokeny łącznie: {sum(lecture_all.values()):,})\n")
    report.append("## Wynik globalny\n")
    report.append(f"- Pokrycie słów-kluczy testu przez wykłady: **{overall_cov:.1f}%**")
    report.append(f"- Podobieństwo kosinusowe (częstości tokenów): **{overall_cos:.1f}%**\n")

    report.append("## Najlepiej pokrywające wykłady (ranking)\n")
    report.append("| PDF | Pokrycie | Podobieństwo | Liczba tokenów |")
    report.append("|---|---:|---:|---:|")
    for name, cov, cos, tok in per_doc:
        report.append(f"| {name} | {cov:.1f}% | {cos:.1f}% | {tok:,} |")
    report.append("")

    report.append("## Top słowa-klucze w teście\n")
    for t, c in top_keywords(test_stats.tokens, k=50):
        report.append(f"- {t} ({c})")
    report.append("")

    report.append("## Top braki (częste w teście, niewystępujące w W1–W11)\n")
    for t, c in missing[:60]:
        report.append(f"- {t} ({c})")
    report.append("")

    out_path = WORKSPACE / "RAPORT_POKRYCIA_W1_W11_vs_test.md"
    out_path.write_text("\n".join(report), encoding="utf-8")
    print(f"Zapisano: {out_path}")
    print(f"Pokrycie (keywords): {overall_cov:.1f}% | Podobieństwo (cosine): {overall_cos:.1f}%")


if __name__ == "__main__":
    main()


