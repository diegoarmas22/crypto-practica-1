from collections import Counter, defaultdict
import string
from break_caesar import FREQ_TABLES


def report(ciphertext: str, language: str = "en") -> str:
    clean = "".join(c for c in ciphertext.upper() if "A" <= c <= "Z")
    n = len(clean)
    if n == 0:
        return "Empty ciphertext."

    ref_table = FREQ_TABLES.get(language, FREQ_TABLES["en"])
    expected_ranking = sorted(
        ref_table.keys(), key=lambda c: ref_table[c], reverse=True
    )

    #unigram counts and ranking
    counts = Counter(clean)
    ranked_cipher = [c for c, _ in counts.most_common()]

    lines = [
        "=" * 60,
        f"CRYPTANALYSIS ASSISTANT REPORT ({language.upper()}) - Length: {n}",
        "=" * 60,
        "",
        "--- LETTER FREQUENCIES & RANK ALIGNMENT ---",
        f"{'CT':<4}{'Count':<8}{'Pct':<8}{'|':<3}{'Ref':<5}{'Expected Pct'}",
        "-" * 45,
    ]

    for i in range(26):
        ct_char = ranked_cipher[i] if i < len(ranked_cipher) else "-"
        ct_cnt = counts[ct_char] if ct_char != "-" else 0
        ct_pct = (ct_cnt / n) * 100 if ct_char != "-" else 0.0

        ref_char = expected_ranking[i]
        ref_pct = ref_table[ref_char] * 100

        lines.append(
            f"{ct_char:<4}{ct_cnt:<8}{ct_pct:>5.2f}%  |   {ref_char:<5}{ref_pct:>5.2f}%"
        )

    #repeated trigrams with positions
    trigram_positions = defaultdict(list)
    for i in range(len(clean) - 2):
        tri = clean[i : i + 3]
        trigram_positions[tri].append(i)

    repeated_trigrams = {
        tri: pos for tri, pos in trigram_positions.items() if len(pos) > 1
    }

    lines.append("\n--- REPEATED TRIGRAMS (Count & 0-indexed Positions) ---")
    if repeated_trigrams:
        for tri, pos in sorted(
            repeated_trigrams.items(), key=lambda x: len(x[1]), reverse=True
        ):
            lines.append(f"{tri}: count={len(pos)}, positions={pos}")
    else:
        lines.append("None found.")

    #top 10 bigrams
    bigrams = Counter(clean[i : i + 2] for i in range(len(clean) - 1))
    lines.append("\n--- TOP 10 BIGRAMS ---")
    for bi, count in bigrams.most_common(10):
        lines.append(f"{bi}: {count}")

    #doubled letters
    doubles = Counter(
        clean[i : i + 2]
        for i in range(len(clean) - 1)
        if clean[i] == clean[i + 1]
    )
    lines.append("\n--- DOUBLE LETTERS ---")
    if doubles:
        for d, count in doubles.most_common():
            lines.append(f"{d}: {count}")
    else:
        lines.append("None found.")

    #suggested initial mapping
    mapping_pairs = [
        f"{ranked_cipher[i]}->{expected_ranking[i]}"
        for i in range(min(len(ranked_cipher), len(expected_ranking)))
    ]
    lines.append("\n--- SUGGESTED INITIAL MAPPING (By Frequency Rank) ---")
    lines.append(", ".join(mapping_pairs))
    lines.append("=" * 60)

    return "\n".join(lines)